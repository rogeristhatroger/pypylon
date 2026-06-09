/*!
\file
\brief Contains the class CEnumEntryParameter added to pypylon for providing backwarts compatibility and
       a consistent parameter access.
*/

#ifndef INCLUDED_BASLER_PYLON_CENUMENTRYPARAMETER_H
#define INCLUDED_BASLER_PYLON_CENUMENTRYPARAMETER_H

#pragma once

#include <pylon/PylonBase.h>
#include <GenApi/IEnumEntry.h>
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
    \brief Extends the GenApi::IEnumEntry interface with IValueEx convenience methods.
    */
    PYLON_INTERFACE IEnumEntryEx : virtual public GenApi::IEnumEntry, virtual public IValueEx
    {
    };


    /*!
    \brief CEnumEntryParameter class used to simplify access to %GenApi enum entry parameters.
           Although this type of parameter is not commonly used, it is provided for backwards compatibility
           and to provide a consistent parameter access. You can cover most use cases using CEnumParameter alone.

    This is a header-only class. The IEnumEntry methods are implemented via the typed
    m_pFeature pointer set during construction or attachment.
    */
    class CEnumEntryParameter : virtual public IEnumEntryEx, public CParameter
    {
    public:
        /*!
        \brief Creates an empty CEnumEntryParameter object.
        \error
            Does not throw C++ exceptions.
        */
        CEnumEntryParameter()
            : m_pFeature( nullptr )
        {
        }


        /*!
        \brief Creates a CEnumEntryParameter object and attaches it to a node, typically retrieved for a nodemap calling GetNode().
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
        explicit CEnumEntryParameter( GenApi::INode* pNode )
        {
            this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
        }


        /*!
        \brief Creates a CEnumEntryParameter object and attaches it to a node of a matching type.
        \param[in] pEnumEntry The node to attach.
        \post
            The parameter object must not be used to access the node's functionality if the source of the attached \c pEnumEntry has been destroyed. In this case, call Release() or attach a new node.
        \error
            Does not throw C++ exceptions.
        */
        explicit CEnumEntryParameter( GenApi::IEnumEntry* pEnumEntry )
        {
            if ( pEnumEntry )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pEnumEntry->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Creates a CEnumEntryParameter object and attaches it to a node retrieved from the provided node map.
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
        CEnumEntryParameter( GenApi::INodeMap* pNodeMap, const char* pName )
        {
            if ( pNodeMap && pName )
            {
                GenApi::INode* pNode = pNodeMap->GetNode( pName );
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Creates a CEnumEntryParameter object and attaches it to a node retrieved from the provided node map.
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
        CEnumEntryParameter( GenApi::INodeMap& nodeMap, const char* pName )
        {
            if ( pName )
            {
                GenApi::INode* pNode = nodeMap.GetNode( pName );
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Copies a CEnumEntryParameter object.
        \param[in] rhs The object to copy.
        \error
            Does not throw C++ exceptions.
        */
        CEnumEntryParameter( const CEnumEntryParameter& rhs )
        {
            if ( rhs.m_pValue )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( rhs.m_pValue->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Destroys the CEnumEntryParameter object.
        Does not access the attached node.
        \error
            Does not throw C++ exceptions.
        */
        virtual ~CEnumEntryParameter()
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
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
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
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
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
            this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pNode );
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a node of the same type to the parameter object.
        \param[in] pEnumEntry The node to assign.
        \return Returns true if the node has been attached.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Attach( GenApi::IEnumEntry* pEnumEntry )
        {
            if ( pEnumEntry )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( pEnumEntry->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a CEnumEntryParameter object.
        \param[in] rhs The object to assign.
        \error
            Does not throw C++ exceptions.
        */
        CEnumEntryParameter& operator=( const CEnumEntryParameter& rhs )
        {
            if ( &rhs != this )
            {
                if ( rhs.m_pValue )
                {
                    // Adds additional safety by indirection, source could be a wrapper
                    this->m_pValue = m_pFeature = dynamic_cast<GenApi::IEnumEntry*>( rhs.m_pValue->GetNode() );
                }
                else
                {
                    this->m_pValue = m_pFeature = nullptr;
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
        virtual bool Equals( const CEnumEntryParameter& rhs ) const
        {
            return this->m_pValue == rhs.m_pValue;
        }


        /*!
        \brief Returns true if the attached node pointer is equal.
        \param[in] pNode The node to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const GenApi::INode* pNode ) const
        {
            if ( this->m_pValue == nullptr && pNode == nullptr )
            {
                return true;
            }
            else if ( this->m_pValue && pNode )
            {
                return this->m_pValue == dynamic_cast<const GenApi::IValue*>( pNode );
            }
            return false;
        }


        /*!
        \brief Returns true if the attached node pointer is equal.
        \param[in] pEnumEntry The node to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const GenApi::IEnumEntry* pEnumEntry ) const
        {
            return this->m_pValue == pEnumEntry;
        }


        /*!
        \brief Releases the attached node.
        \error
            Does not throw C++ exceptions.
        */
        virtual void Release()
        {
            m_pFeature = nullptr;
            CParameter::Release();
        }


        // Implements IValueEx
        virtual bool IsValid() const
        {
            // Both must be set or both must be nullptr
            return ( m_pValue != nullptr && m_pFeature != nullptr );
        }


        // Implements GenApi::IEnumEntry
        //! Get the numeric enum value.
        virtual int64_t GetValue()
        {
            if ( m_pFeature )
            {
                return m_pFeature->GetValue();
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CEnumEntryParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements GenApi::IEnumEntry
        //! Get the symbolic enum value.
        virtual GENICAM_NAMESPACE::gcstring GetSymbolic() const
        {
            if ( m_pFeature )
            {
                return m_pFeature->GetSymbolic();
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CEnumEntryParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements GenApi::IEnumEntry
        //! Get the double number associated with the entry.
        virtual double GetNumericValue()
        {
            if ( m_pFeature )
            {
                return m_pFeature->GetNumericValue();
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CEnumEntryParameter::%hs. (No node attached.)", __func__ );
        }


        // Implements GenApi::IEnumEntry
        //! Indicates if the corresponding EnumEntry is self clearing.
        virtual bool IsSelfClearing()
        {
            if ( m_pFeature )
            {
                return m_pFeature->IsSelfClearing();
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CEnumEntryParameter::%hs. (No node attached.)", __func__ );
        }


    protected:
        GenApi::IEnumEntry* m_pFeature;
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

#endif /* INCLUDED_BASLER_PYLON_CENUMENTRYPARAMETER_H */
