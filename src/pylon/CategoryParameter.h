/*!
\file
\brief Contains the class CCategoryParameter added to pypylon for providing backwards compatibility and
       a consistent parameter access.
*/

#ifndef INCLUDED_BASLER_PYLON_CCATEGORYPARAMETER_H
#define INCLUDED_BASLER_PYLON_CCATEGORYPARAMETER_H

#pragma once

#include <pylon/PylonBase.h>
#include <GenApi/ICategory.h>
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
    \brief Extends the GenApi::ICategory interface with IValueEx convenience methods.
    */
    PYLON_INTERFACE ICategoryEx : virtual public GenApi::ICategory, virtual public IValueEx
    {
    };


    /*!
    \brief CCategoryParameter class used to simplify access to %GenApi category parameters.
           This is a header-only class. The ICategory methods are implemented via the typed
           m_pFeature pointer set during construction or attachment.
    */
    class CCategoryParameter : virtual public ICategoryEx, public CParameter
    {
    public:
        /*!
        \brief Creates an empty CCategoryParameter object.
        \error
            Does not throw C++ exceptions.
        */
        CCategoryParameter()
            : m_pFeature( nullptr )
        {
        }


        /*!
        \brief Creates a CCategoryParameter object and attaches it to a node, typically retrieved for a nodemap calling GetNode().
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
        explicit CCategoryParameter( GenApi::INode* pNode )
        {
            this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
        }


        /*!
        \brief Creates a CCategoryParameter object and attaches it to a node of a matching type.
        \param[in] pCategory The node to attach.
        \post
            The parameter object must not be used to access the node's functionality if the source of the attached \c pCategory has been destroyed. In this case, call Release() or attach a new node.
        \error
            Does not throw C++ exceptions.
        */
        explicit CCategoryParameter( GenApi::ICategory* pCategory )
        {
            if ( pCategory )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pCategory->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Creates a CCategoryParameter object and attaches it to a node retrieved from the provided node map.
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
        CCategoryParameter( GenApi::INodeMap* pNodeMap, const char* pName )
        {
            if ( pNodeMap && pName )
            {
                GenApi::INode* pNode = pNodeMap->GetNode( pName );
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Creates a CCategoryParameter object and attaches it to a node retrieved from the provided node map.
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
        CCategoryParameter( GenApi::INodeMap& nodeMap, const char* pName )
        {
            if ( pName )
            {
                GenApi::INode* pNode = nodeMap.GetNode( pName );
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Copies a CCategoryParameter object.
        \param[in] rhs The object to copy.
        \error
            Does not throw C++ exceptions.
        */
        CCategoryParameter( const CCategoryParameter& rhs )
        {
            if ( rhs.m_pValue )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( rhs.m_pValue->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
        }


        /*!
        \brief Destroys the CCategoryParameter object.
        Does not access the attached node.
        \error
            Does not throw C++ exceptions.
        */
        virtual ~CCategoryParameter()
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
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
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
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
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
            this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pNode );
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a node of the same type to the parameter object.
        \param[in] pCategory The node to assign.
        \return Returns true if the node has been attached.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Attach( GenApi::ICategory* pCategory )
        {
            if ( pCategory )
            {
                // Adds additional safety by indirection, source could be a wrapper
                this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( pCategory->GetNode() );
            }
            else
            {
                this->m_pValue = m_pFeature = nullptr;
            }
            return m_pFeature != nullptr;
        }


        /*!
        \brief Assigns a CCategoryParameter object.
        \param[in] rhs The object to assign.
        \error
            Does not throw C++ exceptions.
        */
        CCategoryParameter& operator=( const CCategoryParameter& rhs )
        {
            if ( &rhs != this )
            {
                if ( rhs.m_pValue )
                {
                    // Adds additional safety by indirection, source could be a wrapper
                    this->m_pValue = m_pFeature = dynamic_cast<GenApi::ICategory*>( rhs.m_pValue->GetNode() );
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
        virtual bool Equals( const CCategoryParameter& rhs ) const
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
        \param[in] pCategory The node to compare to.
        \error
            Does not throw C++ exceptions.
        */
        virtual bool Equals( const GenApi::ICategory* pCategory ) const
        {
            return this->m_pValue == pCategory;
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


        // Implements GenApi::ICategory
        //! Get all features of the category (including sub-categories).
        virtual void GetFeatures( GenApi::FeatureList_t& features ) const
        {
            if ( m_pFeature )
            {
                m_pFeature->GetFeatures( features );
                return;
            }
            throw ACCESS_EXCEPTION( "Parameter not found in CCategoryParameter::%hs. (No node attached.)", __func__ );
        }


    protected:
        GenApi::ICategory* m_pFeature;
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

#endif /* INCLUDED_BASLER_PYLON_CCATEGORYPARAMETER_H */
