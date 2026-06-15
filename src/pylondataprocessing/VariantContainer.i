%rename(VariantContainer) Pylon::DataProcessing::CVariantContainer;
%rename(Variant) Pylon::DataProcessing::CVariant;

%ignore begin;
%ignore end;
%ignore find;
%ignore erase(const CVariantContainer::iterator& it);
%ignore operator[](const String_t& key);
%ignore operator++();
%ignore operator++(int);
%ignore keyvalue_pair;
%ignore iterator;
%ignore CVariantContainer(CVariantContainer &&);

%warnfilter(389) CVariantContainer;
%warnfilter(383) CVariantContainer;

%include <pylondataprocessing/VariantContainer.h>
