#pragma once

namespace Pylon
{
    enum ENodeMapType
    {
        NodeMapType_Camera,
        NodeMapType_StreamGrabber,
        NodeMapType_DeviceTransportLayer,
        NodeMapType_EventGrabber,
        NodeMapType_InstantCamera,
        NodeMapType_ImageFormatConverter,
        NodeMapType_ChunkData,
        NodeMapType_Interface,
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
            m_pNodeMap->GetNodes( Nodes );
        }

        // this method will be ignored by SWIG.
        GENAPI_NAMESPACE::INode* GetNode( const GENICAM_NAMESPACE::gcstring& Name ) const override
        {
            return m_pNodeMap->GetNode( Name );
        }

        GENAPI_NAMESPACE::INode* GetNode2( const GENICAM_NAMESPACE::gcstring& Name, bool throwIfNotFound) const
        {
            GENAPI_NAMESPACE::INode* pNode = m_pNodeMap->GetNode( Name );
            if (throwIfNotFound && pNode == nullptr)
            {
                // trowing an exception is the behavior of genicam.INodeMap.GetNode.
                // this is not always desirable, so we provide the option to return None instead.
                GENICAM_NAMESPACE::gcstring errorMsg = "Node '" + Name + "' not found in nodemap of type " + GetNodeMapTypeString();
                throw GENICAM_NAMESPACE::LogicalErrorException(errorMsg.c_str(), __FILE__, __LINE__);
            }
            return pNode;
        }

        void InvalidateNodes() const override
        {
            m_pNodeMap->InvalidateNodes();
        }

        bool Connect( GENAPI_NAMESPACE::IPort* pPort, const GENICAM_NAMESPACE::gcstring& PortName ) const override
        {
            return m_pNodeMap->Connect( pPort, PortName );
        }

        bool Connect( GENAPI_NAMESPACE::IPort* pPort ) const override
        {
            return m_pNodeMap->Connect( pPort );
        }

        bool Connect( GENAPI_NAMESPACE::IPortStacked* pPort ) override
        {
            return m_pNodeMap->Connect( pPort );
        }

        bool Connect( GENAPI_NAMESPACE::IPortStacked* pPort, const GENICAM_NAMESPACE::gcstring& PortName ) override
        {
            return m_pNodeMap->Connect( pPort, PortName );
        }

        GENAPI_NAMESPACE::CNodeWriteConcatenator* NewNodeWriteConcatenator() const override
        {
            return m_pNodeMap->NewNodeWriteConcatenator();
        }

        bool ConcatenatedWrite( GENAPI_NAMESPACE::CNodeWriteConcatenator* pConcatenator, bool featureStreaming = true, GENICAM_NAMESPACE::gcstring_vector* pErrorList = NULL ) override
        {
            return m_pNodeMap->ConcatenatedWrite( pConcatenator, featureStreaming, pErrorList );
        }

        void SetSuppressCallbackMode( GENAPI_NAMESPACE::ECallbackSuppressMode mode ) override
        {
            m_pNodeMap->SetSuppressCallbackMode( mode );
        }

        GENICAM_NAMESPACE::gcstring GetDeviceName() override
        {
            return m_pNodeMap->GetDeviceName();
        }

        void Poll( int64_t ElapsedTime ) override
        {
            m_pNodeMap->Poll( ElapsedTime );
        }

        GENAPI_NAMESPACE::CLock& GetLock() const override
        {
            return m_pNodeMap->GetLock();
        }

        uint64_t GetNumNodes() const override
        {
            return m_pNodeMap->GetNumNodes();
        }

        bool ParseSwissKnifes( GENICAM_NAMESPACE::gcstring_vector* pErrorList = NULL ) const override
        {
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
            case NodeMapType_Unknown:
            default:
                return "Unknown";
            }
        }

    protected:
        virtual GENICAM_NAMESPACE::gcstring GetModelName() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetModelName();
        }

        virtual GENICAM_NAMESPACE::gcstring GetVendorName() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetVendorName();
        }

        virtual GENICAM_NAMESPACE::gcstring GetToolTip() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetToolTip();
        }

        virtual GENICAM_NAMESPACE::gcstring GetStandardNameSpace() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetStandardNameSpace();
        }

        virtual void GetGenApiVersion(Version_t &Version, uint16_t &Build) override
        {
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetGenApiVersion(Version, Build);
        }

        virtual void GetSchemaVersion(Version_t &Version) override
        {
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetSchemaVersion(Version);
        }

        virtual void GetDeviceVersion(Version_t &Version) override
        {
            dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetDeviceVersion(Version);
        }

        virtual GENICAM_NAMESPACE::gcstring GetProductGuid() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetProductGuid();
        }

        virtual GENICAM_NAMESPACE::gcstring GetVersionGuid() override
        {
            return dynamic_cast<GENAPI_NAMESPACE::IDeviceInfo*>(m_pNodeMap)->GetVersionGuid();
        }
    private:
        GENAPI_NAMESPACE::INodeMap* m_pNodeMap = nullptr;
        ENodeMapType m_nodeMapType = NodeMapType_Unknown;
    };
}
