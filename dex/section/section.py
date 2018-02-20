# -- coding: utf-8 --

from section_base import *
from section_map_item import *
from section_header import *
from section_string_id import *
from section_type_id import *
from section_proto_id import *
from section_field_id import *
from section_method_id import *
from section_class_def import *
from section_type_list import *
from section_class_data import *
from section_annotation_set_ref_list import *
from section_annotation_set_item import *
from section_annotation_item import *
from section_string_list import *
from section_encoded_array import *
from section_annotations_directory import *
from section_code import *
from section_debug_info import *

'''
section中的映射表: (类型，Section类)
'''
section_class_map = {
	
	TYPE_HEADER_ITEM                   :    HeaderSection,
	TYPE_STRING_ID_ITEM                :    StringIdListSection,
	TYPE_TYPE_ID_ITEM                  :    TypeIdListSection,
	TYPE_PROTO_ID_ITEM                 :    ProtoIdListSection,
	TYPE_FIELD_ID_ITEM                 :    FieldIdListSection,
	TYPE_METHOD_ID_ITEM                :    MethodIdListSection,
	TYPE_CLASS_DEF_ITEM                :    ClassDefListSection,
	TYPE_MAP_LIST                      :    MapItemListSection,
	TYPE_TYPE_LIST                     :    TypeListSection,
	TYPE_ANNOTATION_SET_REF_LIST       :    AnnotationSetRefListSection,
	TYPE_ANNOTATION_SET_ITEM           :    AnnotationSetItemSection,
	TYPE_CLASS_DATA_ITEM               :    ClassDataListSection,
	TYPE_CODE_ITEM                     :    CodeSection,
	TYPE_STRING_DATA_ITEM              :    StringListSection,
	TYPE_DEBUG_INFO_ITEM               :    DebugInfoSection,
	TYPE_ANNOTATION_ITEM               :    AnnotationItemSection,
	TYPE_ENCODED_ARRAY_ITEM            :    EncodedArraySection,
	TYPE_ANNOTATIONS_DIRECTORY_ITEM    :    AnnotationsDirectorySection,

}