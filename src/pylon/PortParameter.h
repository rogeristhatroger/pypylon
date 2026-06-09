/*!
\file
\brief Contains the class CPortParameter added to pypylon for providing backwards compatibility and
       a consistent parameter access.

Note: IPort derives from IBase, not IValue. Therefore CPortParameter does NOT inherit from
CParameter.
*/

#ifndef INCLUDED_BASLER_PYLON_CPORTPARAMETER_H
#define INCLUDED_BASLER_PYLON_CPORTPARAMETER_H

#pragma once

#include <pylon/PylonBase.h>
#include <GenApi/IPort.h>
#include <GenApi/INode.h>
#include <pylon/Parameter.h>
#include <pylon/Platform.h>

#ifdef _MSC_VER
#   pragma pack(push, PYLON_PACKING)
#endif /* _MSC_VER */

#if defined(PYLON_WIN_BUILD)
#   pragma warning( push )
#   pragma warning( disable : 4275 ) // Class needs to have a dll interface to be used by clients of the class.
#   pragma warning( disable : 4250 ) // warning C4250: 'Pylon::CXYZParameter': inherits 'Pylon::CParameter::Pylon::CParameter::ZYX' via dominance
#elif defined(PYLON_UNIX_BUILD)
#   if defined(__clang__)
#       pragma clang diagnostic push
#       pragma clang diagnostic ignored "-Woverloaded-virtual"
#   else
#       pragma GCC diagnostic push
#       pragma GCC diagnostic ignored "-Woverloaded-virtual"
#   endif
#endif

namespace Pylon
{
    /*!
    \brief Extends the GenApi::IPort interface with pylon convenience methods.

    Unlike other parameter interfaces, IPortEx does NOT extend IValueEx because
    IPort is not derived from IValue.
    */
    PYLON_INTERFACE IPortEx : virtual public GenApi::IPort
    {
        /*!
        \brief Indicates whether the parameter is readable.
        \return Returns true if the parameter is readable.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool IsReadable() const = 0;

        /*!
        \brief Indicates whether the parameter is writable.
        \return Returns true if the parameter is writable.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool IsWritable() const = 0;

        /*!
        \brief Indicates whether a node is attached.
        \return Returns true if a node is attached.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool IsValid() const = 0;

        /*!
        \brief Returns the underlying GenApi node.
        \error
            Throws an exception if no node is attached.
        */
        virtual GenApi::INode* GetNode() = 0;

        /*!
        \brief Gets the parameter information.
        \param[in] info The type information to return.
        \error
            Throws an exception if no node is attached.
        */
        virtual String_t GetInfo( EParameterInfo info ) = 0;

        /*!
        \brief Gets the parameter information if attached, otherwise returns the default.
        \param[in] info The type information to return.
        \param[in] defaultInfo The default information returned if the parameter is not attached.
        \error
            Can throw exceptions if the retrieval of the information fails.
        */
        virtual String_t GetInfoOrDefault( EParameterInfo info, const String_t defaultInfo ) = 0;
    };


    /*!
    \brief CPortParameter class used to simplify access to %GenApi port parameters.

    This is a header-only class. Because IPort is derived from IBase (not IValue),
    CPortParameter does not inherit from CParameter.
    - ToString() returns a placeholder string of the form "<Port NodeName>".
    - FromString() and IsValueCacheValid() always throw an AccessException.
    - Read() and Write() delegate to the underlying IPort node.
    */
    class CPortParameter : virtual public IPortEx
    {
    public:
        /*!
        \brief Creates an empty CPortParameter object.
        \error
            Does not throw C++ exceptions.
        */
        CPortParameter()
            : m_pFeature( nullptr )
            , m_pNode( nullptr )
        {
        }


        /*!
        \brief Creates a CPortParameter object and attaches it to a node, typically retrieved for a nodemap calling GetNode().
        \param[in] pNode The node to attach.
        \post
        <ul>
        <li>If the passed node does not match the parameter type, the parameter will be empty, see IsValid().
        <li>If the passed node does match the parameter type, it is attached and the parameter object can be used to access the node's functionality.
        <li>The parameter object must not be used to access the node's functionality if the source of the attached \c pNode has been destroyed. In this case, call Release() or attach a new node.
        </ul>
        \error
            Does not throw C++ exceptions.
        */
        explicit CPortParameter( GenApi::INode* pNode )
        {
            m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
            m_pNode    = m_pFeature ? pNode : nullptr;
        }


        /*!
        \brief Creates a CPortParameter object and attaches it to a node of a matching type.
        \param[in] pPort The node to attach.
        \post
            The parameter object must not be used to access the node's functionality if the source of the attached \c pPort has been destroyed. In this case, call Release() or attach a new node.
        \error
            Does not throw C++ exceptions.
        */
        explicit CPortParameter( GenApi::IPort* pPort )
        {
            if ( pPort )
            {
                // Cross-cast to INode* for node metadata access
                m_pNode    = dynamic_cast<GenApi::INode*>( pPort );
                m_pFeature = m_pNode ? dynamic_cast<GenApi::IPort*>( m_pNode ) : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
        }


        /*!
        \brief Creates a CPortParameter object and attaches it to a node retrieved from the provided node map.
        \param[in] pNodeMap The node map. The source of the parameter.
        \param[in] pName The name of the parameter to attach.
        \post
        <ul>
        <li>If \c pNodeMap or \c name is nullptr, the parameter will be empty, see IsValid().
        <li>If the node does not match the parameter type, the parameter will be empty, see IsValid().
        <li>If the node does match the parameter type, it is attached and the parameter object can be used to access the node's functionality.
        <li>The parameter object must not be used to access the node's functionality if the provided node map has been destroyed. In this case, call Release() or attach a new node.
        </ul>
        \error
            The call to GenApi::INodeMap::GetNode can throw C++ exceptions.
        */
        CPortParameter( GenApi::INodeMap* pNodeMap, const char* pName )
        {
            if ( pNodeMap && pName )
            {
                GenApi::INode* pNode = pNodeMap->GetNode( pName );
                m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
                m_pNode    = m_pFeature ? pNode : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
        }


        /*!
        \brief Creates a CPortParameter object and attaches it to a node retrieved from the provided node map.
        \param[in] nodeMap The node map. The source of the parameter.
        \param[in] pName The name of the parameter to attach.
        \post
        <ul>
        <li>If \c name is nullptr, the parameter will be empty, see IsValid().
        <li>If the node does not match the parameter type, the parameter will be empty, see IsValid().
        <li>If the node does match the parameter type, it is attached and the parameter object can be used to access the node's functionality.
        <li>The parameter object must not be used to access the node's functionality if the provided node map has been destroyed. In this case, call Release() or attach a new node.
        </ul>
        \error
            The call to GenApi::INodeMap::GetNode can throw C++ exceptions.
        */
        CPortParameter( GenApi::INodeMap& nodeMap, const char* pName )
        {
            if ( pName )
            {
                GenApi::INode* pNode = nodeMap.GetNode( pName );
                m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
                m_pNode    = m_pFeature ? pNode : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
        }


        /*!
        \brief Copies a CPortParameter object.
        \param[in] rhs The object to copy.
        \error
            Does not throw C++ exceptions.
        */
        CPortParameter( const CPortParameter& rhs )
        {
            if ( rhs.m_pNode )
            {
                // Re-derive from the node for safety
                m_pFeature = dynamic_cast<GenApi::IPort*>( rhs.m_pNode );
                m_pNode    = m_pFeature ? rhs.m_pNode : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
        }


        /*!
        \brief Destroys the CPortParameter object.
        Does not access the attached node.
        \error
            Does not throw C++ exceptions.
        */
        virtual ~CPortParameter()
        {
        }


        /*!
        \brief Attaches a node retrieved from the provided node map.
        \param[in] pNodeMap The node map. The source of the parameter.
        \param[in] pName The name of the parameter to attach.
        \return Returns true if the node has been attached.
        \error
            The call to GenApi::INodeMap::GetNode can throw C++ exceptions.
        */
        virtual bool Attach( GenApi::INodeMap* pNodeMap, const char* pName )
        {
            if ( pNodeMap && pName )
            {
                GenApi::INode* pNode = pNodeMap->GetNode( pName );
                m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
                m_pNode    = m_pFeature ? pNode : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
            return m_pFeature != nullptr;
        }


        /*!
        \brief Attaches a node retrieved from the provided node map.
        \param[in] nodeMap The node map. The source of the parameter.
        \param[in] pName The name of the parameter to attach.
        \return Returns true if the node has been attached.
        \error
            The call to GenApi::INodeMap::GetNode can throw C++ exceptions.
        */
        virtual bool Attach( GenApi::INodeMap& nodeMap, const char* pName )
        {
            if ( pName )
            {
                GenApi::INode* pNode = nodeMap.GetNode( pName );
                m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
                m_pNode    = m_pFeature ? pNode : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
            return m_pFeature != nullptr;
        }


        /*!
        \brief Attaches a node, typically retrieved for a nodemap calling GetNode().
        \param[in] pNode The node to assign.
        \return Returns true if the node has been attached.
        \post
        <ul>
        <li>If the node does not match the parameter type, the parameter will be empty, see IsValid().
        <li>If the node does match the parameter type, it is attached and the parameter object can be used to access the node's functionality.
        </ul>
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Attach( GenApi::INode* pNode )
        {
            m_pFeature = dynamic_cast<GenApi::IPort*>( pNode );
            m_pNode    = m_pFeature ? pNode : nullptr;
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a node of the same type to the parameter object.
        \param[in] pPort The node to assign.
        \return Returns true if the node has been attached.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Attach( GenApi::IPort* pPort )
        {
            if ( pPort )
            {
                // Cross-cast to INode* for node metadata access
                m_pNode    = dynamic_cast<GenApi::INode*>( pPort );
                m_pFeature = m_pNode ? dynamic_cast<GenApi::IPort*>( m_pNode ) : nullptr;
            }
            else
            {
                m_pFeature = nullptr;
                m_pNode    = nullptr;
            }
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a CPortParameter object.
        \param[in] rhs The object to assign.
        \error
            Does not throw C++ exceptions.
        */
        CPortParameter& operator=( const CPortParameter& rhs )
        {
            if ( &rhs != this )
            {
                if ( rhs.m_pNode )
                {
                    m_pFeature = dynamic_cast<GenApi::IPort*>( rhs.m_pNode );
                    m_pNode    = m_pFeature ? rhs.m_pNode : nullptr;
                }
                else
                {
                    m_pFeature = nullptr;
                    m_pNode    = nullptr;
                }
            }
            return *this;
        }


        /*!
        \brief Returns true if the same nodes are attached or both parameters are empty.
        \param[in] rhs The object to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const CPortParameter& rhs ) const
        {
            return this->m_pNode == rhs.m_pNode;
        }


        /*!
        \brief Returns true if the attached node pointer is equal.
        \param[in] pNode The node to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const GenApi::INode* pNode ) const
        {
            return this->m_pNode == pNode;
        }


        /*!
        \brief Returns true if the attached node pointer is equal.
        \param[in] pPort The node to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const GenApi::IPort* pPort ) const
        {
            return this->m_pFeature == pPort;
        }


        /*!
        \brief Releases the attached node.
        \error
            Does not throw C++ exceptions.
        */
        virtual void Release()
        {
            m_pFeature = nullptr;
            m_pNode    = nullptr;
        }


        // Implements IPortEx
        virtual bool IsValid() const
        {
            // Both must be set or both must be nullptr
            return ( m_pFeature != nullptr && m_pNode != nullptr );
        }


        // Implements IPortEx
        virtual bool IsReadable() const
        {
            bool result = false;
            try
            {
                result = GenApi::IsReadable( m_pFeature );
            }
            catch ( ... )
            {
            }
            return result;
        }


        // Implements IPortEx
        virtual bool IsWritable() const
        {
            bool result = false;
            try
            {
                result = GenApi::IsWritable( m_pFeature );
            }
            catch ( ... )
            {
            }
            return result;
        }


        // Implements IPortEx
        virtual GenApi::INode* GetNode()
        {
            if ( m_pNode )
            {
                return m_pNode;
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CPortParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements IPortEx
        virtual String_t GetInfo( EParameterInfo info )
        {
            if ( m_pNode )
            {
                String_t result;
                switch ( info )
                {
                    case ParameterInfo_Name:        result = m_pNode->GetName();        break;
                    case ParameterInfo_DisplayName: result = m_pNode->GetDisplayName(); break;
                    case ParameterInfo_ToolTip:     result = m_pNode->GetToolTip();     break;
                    case ParameterInfo_Description: result = m_pNode->GetDescription(); break;
                    default:
                        throw INVALID_ARGUMENT_EXCEPTION( "Invalid value for EParameterInfo passed to CPortParameter::%hs.", __func__ );
                }
                return result;
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CPortParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements IPortEx
        virtual String_t GetInfoOrDefault( EParameterInfo info, const String_t defaultInfo )
        {
            if ( m_pNode )
            {
                try
                {
                    return GetInfo( info );
                }
                catch ( ... )
                {
                }
            }
            return defaultInfo;
        }


        // Implements IBase
        virtual GenApi::EAccessMode GetAccessMode() const
        {
            if ( m_pFeature )
            {
                return m_pFeature->GetAccessMode();
            }
            return GenApi::NI;
        }

        // Implements GenApi::IPort
        //! Reads a chunk of bytes from the port.
        virtual void Read( void* pBuffer, int64_t Address, int64_t Length )
        {
            if ( m_pFeature )
            {
                m_pFeature->Read( pBuffer, Address, Length );
                return;
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CPortParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements GenApi::IPort
        //! Writes a chunk of bytes to the port.
        virtual void Write( const void* pBuffer, int64_t Address, int64_t Length )
        {
            if ( m_pFeature )
            {
                m_pFeature->Write( pBuffer, Address, Length );
                return;
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CPortParameter::%hs. (No node attached.)", __func__ );
        }

        // The following messages have been added here for backwards compatibility.
        //! Get the Id of the chunk the port should be attached to
        virtual GENICAM_NAMESPACE::gcstring GetChunkID() const
        {
            if ( m_pFeature )
            {
                auto pChunkPort = dynamic_cast<const GENAPI_NAMESPACE::IChunkPort*>(m_pFeature);
                if (pChunkPort)
                {
                    return pChunkPort->GetChunkID();
                }
                else
                {
                    throw DYNAMICCAST_EXCEPTION("CPortParameter::GetChunkID: object does not implement IChunkPort");
                }
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CPortParameter::%hs. (No node attached.)", __func__ );
        }

        virtual GENAPI_NAMESPACE::EYesNo CacheChunkData() const
        {
            if (m_pFeature)
            {
                auto pChunkPort = dynamic_cast<const GENAPI_NAMESPACE::IChunkPort*>(m_pFeature);
                if (pChunkPort)
                {
                    return pChunkPort->CacheChunkData();
                }
                else
                {
                    throw DYNAMICCAST_EXCEPTION("CPortParameter::CacheChunkData: object does not implement IChunkPort");
                }
            }
            throw ACCESS_EXCEPTION("Parameter not found in CPortParameter::%hs. (No node attached.)", __func__);
        }

        //! Determines if the port adapter must perform an endianess swap
        virtual GENAPI_NAMESPACE::EYesNo GetSwapEndianess()
        {
            if (m_pFeature)
            {
                auto pPortConstruct = dynamic_cast<GENAPI_NAMESPACE::IPortConstruct*>(m_pFeature);
                if (pPortConstruct)
                {
                    return pPortConstruct->GetSwapEndianess();
                }
                else
                {
                    throw DYNAMICCAST_EXCEPTION(
                        "CPortParameter::GetSwapEndianess: object does not implement IPortConstruct");
                }
            }
            throw ACCESS_EXCEPTION("Parameter not found in CPortParameter::%hs. (No node attached.)", __func__);
        }

    protected:
        GenApi::IPort* m_pFeature;  ///< Typed pointer for IPort operations.
        GenApi::INode* m_pNode;     ///< Node pointer for metadata access (GetNode, GetInfo, ToString).
    };
}

#if defined(PYLON_WIN_BUILD)
#   pragma warning( pop )
#elif defined(PYLON_UNIX_BUILD)
#   if defined(__clang__)
#       pragma clang diagnostic pop
#   else
#       pragma GCC diagnostic pop
#   endif
#endif

#ifdef _MSC_VER
#   pragma pack(pop)
#endif /* _MSC_VER */

#endif /* INCLUDED_BASLER_PYLON_CPORTPARAMETER_H */

