# -- coding: utf-8 --

'''
定义section的类型
'''
TYPE_HEADER_ITEM                   =    0x0000
TYPE_STRING_ID_ITEM                =    0x0001
TYPE_TYPE_ID_ITEM                  =    0x0002
TYPE_PROTO_ID_ITEM                 =    0x0003
TYPE_FIELD_ID_ITEM                 =    0x0004
TYPE_METHOD_ID_ITEM                =    0x0005
TYPE_CLASS_DEF_ITEM                =    0x0006
TYPE_MAP_LIST                      =    0x1000
TYPE_TYPE_LIST                     =    0x1001
TYPE_ANNOTATION_SET_REF_LIST       =    0x1002
TYPE_ANNOTATION_SET_ITEM           =    0x1003
TYPE_CLASS_DATA_ITEM               =    0x2000
TYPE_CODE_ITEM                     =    0x2001
TYPE_STRING_DATA_ITEM              =    0x2002
TYPE_DEBUG_INFO_ITEM               =    0x2003
TYPE_ANNOTATION_ITEM               =    0x2004
TYPE_ENCODED_ARRAY_ITEM            =    0x2005
TYPE_ANNOTATIONS_DIRECTORY_ITEM    =    0x2006

'''
类型列表
'''
type_list = [

	TYPE_HEADER_ITEM,
	TYPE_STRING_ID_ITEM,
	TYPE_TYPE_ID_ITEM,
	TYPE_PROTO_ID_ITEM,
	TYPE_FIELD_ID_ITEM,
	TYPE_METHOD_ID_ITEM,
	TYPE_CLASS_DEF_ITEM,
	TYPE_MAP_LIST,
	TYPE_TYPE_LIST,
	TYPE_ANNOTATION_SET_REF_LIST,
	TYPE_ANNOTATION_SET_ITEM,
	TYPE_CLASS_DATA_ITEM,
	TYPE_CODE_ITEM,
	TYPE_STRING_DATA_ITEM,
	TYPE_DEBUG_INFO_ITEM,
	TYPE_ANNOTATION_ITEM,
	TYPE_ENCODED_ARRAY_ITEM,
	TYPE_ANNOTATIONS_DIRECTORY_ITEM,

]

'''
类型的描述表:  (类型， 类型描述)
'''
type_desc_map = {
	
	TYPE_HEADER_ITEM                   :    'HeaderSection',
	TYPE_STRING_ID_ITEM                :    'StringIdListSection',
	TYPE_TYPE_ID_ITEM                  :    'TypeIdListSection',
	TYPE_PROTO_ID_ITEM                 :    'ProtoIdListSection',
	TYPE_FIELD_ID_ITEM                 :    'FieldIdListSection',
	TYPE_METHOD_ID_ITEM                :    'MethodIdListSection',
	TYPE_CLASS_DEF_ITEM                :    'ClassDefListSection',
	TYPE_MAP_LIST                      :    'MapItemListSection',
	TYPE_TYPE_LIST                     :    'TypeListSection',
	TYPE_ANNOTATION_SET_REF_LIST       :    'AnnotationSetRefListSection',
	TYPE_ANNOTATION_SET_ITEM           :    'AnnotationSetItemSection',
	TYPE_CLASS_DATA_ITEM               :    'ClassDataListSection',
	TYPE_CODE_ITEM                     :    'CodeSection',
	TYPE_STRING_DATA_ITEM              :    'StringListSection',
	TYPE_DEBUG_INFO_ITEM               :    'DebugInfoSection',
	TYPE_ANNOTATION_ITEM               :    'AnnotationItemSection',
	TYPE_ENCODED_ARRAY_ITEM            :    'EncodedArraySection',
	TYPE_ANNOTATIONS_DIRECTORY_ITEM    :    'AnnotationsDirectorySection',

}