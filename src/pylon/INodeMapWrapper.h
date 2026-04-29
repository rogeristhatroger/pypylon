#pragma once

namespace Pylon
{
    enum ENodeMapType
    {
        NodeMapType_Camera, // IPylonDevice::GetNodeMap() or CInstantCamera::GetNodeMap()
        NodeMapType_StreamGrabber, // IStreamGrabber::GetNodeMap()
        NodeMapType_DeviceTransportLayer, // IPylonDevice::GetTLNodeMap()
        NodeMapType_EventGrabber, // IEventGrabber::GetNodeMap()
        NodeMapType_InstantCamera, // CInstantCamera::GetInstantCameraNodeMap()
        NodeMapType_ImageFormatConverter, // CImageFormatConverter::GetNodeMap()
        NodeMapType_ChunkData, // CGrabResultData::GetChunkDataNodeMap()
        NodeMapType_Interface, // IInterface::GetNodeMap()
        NodeMapType_TransportLayer, // ITransportLayer::GetNodeMap()
        NodeMapType_Unknown
    };

    // This class is a simple wrapper around an INodeMap pointer. It is used to
    // change the SWIG mapping of GenICam types in the module pypylon.pylon
    // and pypylon.dataprocessing using SWIG typemap instructions.
    class INodeMapWrapper : public GENAPI_NAMESPACE::INodeMap, public GENAPI_NAMESPACE::IDeviceInfo //needed for saving pfs files
    {
    public:
        INodeMapWrapper( GENAPI_NAMESPACE::INodeMap* pNodeMap, ENodeMapType nodeMapType)
            : m_pNodeMap( pNodeMap )
            , m_nodeMapType(nodeMapType)
        {
        }

        virtual ~INodeMapWrapper() = default;

        void GetNodes( GENAPI_NAMESPACE::NodeList_t& Nodes ) const override
        {
            if (m_pNodeMap == nullptr)
            {
                Nodes.clear();
            }
            else
            {
                m_pNodeMap->GetNodes( Nodes );
            }
        }

        // this method will be ignored by SWIG.
        GENAPI_NAMESPACE::INode* GetNode( const GENICAM_NAMESPACE::gcstring& Name ) const override
        {
            if ( m_pNodeMap != nullptr )
            {
                return m_pNodeMap->GetNode( Name );
            }
            else
            {
                return nullptr;
            }
        }

        GENAPI_NAMESPACE::INode* GetNode2( const GENICAM_NAMESPACE::gcstring& Name, bool throwIfNotFound) const
        {
            GENAPI_NAMESPACE::INode* pNode = nullptr;
            if ( m_pNodeMap != nullptr )
            {
                pNode = m_pNodeMap->GetNode( Name );  // result was previously discarded
            }
            if (throwIfNotFound && pNode == nullptr)
            {
                // throwing an exception is the behavior of genicam.INodeMap.GetNode.
                // this is not always desirable, so we provide the option to return None instead.
                GENICAM_NAMESPACE::gcstring errorMsg = "Node '" + Name + "' not found in nodemap of type " + GetNodeMapTypeString();
                throw GENICAM_NAMESPACE::LogicalErrorException(errorMsg.c_str(), __FILE__, __LINE__);
            }
            return pNode;
        }

        bool Contains( const GENICAM_NAMESPACE::gcstring& Name ) const
        {
            if ( m_pNodeMap == nullptr )  // was: pNodeMap (missing m_ prefix)
            {
                return false;
            }
            else
            {
                return m_pNodeMap->GetNode( Name ) != nullptr;
            }
        }

        void InvalidateNodes() const override
        {
            if (m_pNodeMap != nullptr)
            {
                m_pNodeMap->InvalidateNodes();
            }
        }

        bool Connect( GENAPI_NAMESPACE::IPort* pPort, const GENICAM_NAMESPACE::gcstring& PortName ) const override
        {
            CheckNotNull();
            return m_pNodeMap->Connect( pPort, PortName );
        }

        bool Connect( GENAPI_NAMESPACE::IPort* pPort ) const override
        {
            CheckNotNull();
            return m_pNodeMap->Connect( pPort );
        }

        bool Connect( GENAPI_NAMESPACE::IPortStacked* pPort ) override
        {
            CheckNotNull();
            return m_pNodeMap->Connect( pPort );
        }

        bool Connect( GENAPI_NAMESPACE::IPortStacked* pPort, const GENICAM_NAMESPACE::gcstring& PortName ) override
        {
            CheckNotNull();
            return m_pNodeMap->Connect( pPort, PortName );
        }

        GENAPI_NAMESPACE::CNodeWriteConcatenator* NewNodeWriteConcatenator() const override
        {
            CheckNotNull();
            return m_pNodeMap->NewNodeWriteConcatenator();
        }

        bool ConcatenatedWrite( GENAPI_NAMESPACE::CNodeWriteConcatenator* pConcatenator, bool featureStreaming = true, GENICAM_NAMESPACE::gcstring_vector* pErrorList = NULL ) override
        {
            CheckNotNull();
            return m_pNodeMap->ConcatenatedWrite( pConcatenator, featureStreaming, pErrorList );
        }

        void SetSuppressCallbackMode( GENAPI_NAMESPACE::ECallbackSuppressMode mode ) override
        {
            CheckNotNull();
            m_pNodeMap->SetSuppressCallbackMode( mode );
        }

        GENICAM_NAMESPACE::gcstring GetDeviceName() override
        {
            CheckNotNull();
            return m_pNodeMap->GetDeviceName();
        }

        void Poll( int64_t ElapsedTime ) override
        {
            if (m_pNodeMap != nullptr)
            {
                m_pNodeMap->Poll( ElapsedTime );
            }
        }

        GENAPI_NAMESPACE::CLock& GetLock() const override
        {
            CheckNotNull();
            return m_pNodeMap->GetLock();
        }

        uint64_t GetNumNodes() const override
        {
            if (m_pNodeMap == nullptr)
            {
                return 0;
            }
            else
            {
                return m_pNodeMap->GetNumNodes();
            }
        }

        bool ParseSwissKnifes( GENICAM_NAMESPACE::gcstring_vector* pErrorList = NULL ) const override
        {
            CheckNotNull();
            return m_pNodeMap->ParseSwissKnifes( pErrorList );
        }

        GENAPI_NAMESPACE::INodeMap* _Get()
        {
            return m_pNodeMap;
        }

        ENodeMapType GetNodeMapType() const
        {
            return m_nodeMapType;
        }

        GENICAM_NAMESPACE::gcstring GetNodeMapTypeString() const
        {
            switch (m_nodeMapType)
            {
            case NodeMapType_Camera:
                return "Camera";
            case NodeMapType_StreamGrabber:
                return "StreamGrabber";
            case NodeMapType_DeviceTransportLayer:
                return "DeviceTransportLayer";
            case NodeMapType_EventGrabber:
                return "EventGrabber";
            case NodeMapType_InstantCamera:
                return "InstantCamera";
            case NodeMapType_ImageFormatConverter:
                return "ImageFormatConverter";
            case NodeMapType_ChunkData:
                return "ChunkData";
            case NodeMapType_Interface:
                return "Interface";
            case NodeMapType_TransportLayer:
                return "TransportLayer";
            case NodeMapType_Unknown:
            default:
                return "Unknown";
            }
        }

    protected:
        void CheckNotNull() const
        {
            if (m_pNodeMap == nullptr)
            {
                throw GENICAM_NAMESPACE::RuntimeException(
                    ("Operation called on an invalid nodemap of type " + GetNodeMapTypeString()).c_str(),
                    __FILE__, __LINE__
                );
            }
        }

        virtual GENICAM_NAMESPACE::gcstring GetModelName() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetModelName();
        }

        virtual GENICAM_NAMESPACE::gcstring GetVendorName() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetVendorName();
        }

        virtual GENICAM_NAMESPACE::gcstring GetToolTip() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetToolTip();
        }

        virtual GENICAM_NAMESPACE::gcstring GetStandardNameSpace() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetStandardNameSpace();
        }

        virtual void GetGenApiVersion(Version_t &Version, uint16_t &Build) override
        {
            CheckNotNull();
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetGenApiVersion(Version, Build);
        }

        virtual void GetSchemaVersion(Version_t &Version) override
        {
            CheckNotNull();
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetSchemaVersion(Version);
        }

        virtual void GetDeviceVersion(Version_t &Version) override
        {
            CheckNotNull();
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetDeviceVersion(Version);
        }

        virtual GENICAM_NAMESPACE::gcstring GetProductGuid() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetProductGuid();
        }

        virtual GENICAM_NAMESPACE::gcstring GetVersionGuid() override
        {
            CheckNotNull();
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetVersionGuid();
        }
    private:
        GENAPI_NAMESPACE::INodeMap* m_pNodeMap = nullptr;
        ENodeMapType m_nodeMapType = NodeMapType_Unknown;
    };
}
