#pragma once

namespace Pylon
{
    // This class is a simple wrapper around an INodeMap pointer. It is used to
    // change the SWIG mapping of GenICam types in the module pypylon.pylon
    // and pypylon.dataprocessing using SWIG typemap instructions.
    class INodeMapWrapper : public GENAPI_NAMESPACE::INodeMap, public GENAPI_NAMESPACE::IDeviceInfo //needed for saving pfs files
    {
    public:
        INodeMapWrapper( GENAPI_NAMESPACE::INodeMap* pNodeMap )
            : m_pNodeMap( pNodeMap )
        {
        }

        virtual ~INodeMapWrapper() = default;

        void GetNodes( GENAPI_NAMESPACE::NodeList_t& Nodes ) const override
        {
            m_pNodeMap->GetNodes( Nodes );
        }

        GENAPI_NAMESPACE::INode* GetNode( const GENICAM_NAMESPACE::gcstring& Name ) const override
        {
            return m_pNodeMap->GetNode( Name );
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
        GENAPI_NAMESPACE::INodeMap* m_pNodeMap;
    };
}
