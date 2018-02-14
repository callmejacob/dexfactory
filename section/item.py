# -- coding: utf-8 --

from item_base import *
from item_map_list import *
from item_header import *
from item_string_id import *
from item_type_id import *
from item_proto_id import *
from item_field_id import *
from item_method_id import *
from item_class_def import *
from item_type_list import *
from item_string_data import *
from item_class_data import *
from item_annotation_set_ref_list import *
from item_annotation_set_item import *
from item_annotation_item import *
from item_encoded_array import *
from item_annotations_directory import *
from item_code import *
from item_debug_info import *

'''
section中子项类的映射表: (类型，Item类)
'''
item_class_map = {
	
	TYPE_HEADER_ITEM                   :    HeaderItem,
	TYPE_STRING_ID_ITEM                :    StringIdItem,
	TYPE_TYPE_ID_ITEM                  :    TypeIdItem,
	TYPE_PROTO_ID_ITEM                 :    ProtoIdItem,
	TYPE_FIELD_ID_ITEM                 :    FieldIdItem,
	TYPE_METHOD_ID_ITEM                :    MethodIdItem,
	TYPE_CLASS_DEF_ITEM                :    ClassDefItem,
	TYPE_MAP_LIST                      :    MapListItem,
	TYPE_TYPE_LIST                     :    TypeListItem,
	TYPE_ANNOTATION_SET_REF_LIST       :    AnnotationSefRefListItem,
	TYPE_ANNOTATION_SET_ITEM           :    AnnotationSetItemItem,
	TYPE_CLASS_DATA_ITEM               :    ClassDataItem,
	TYPE_CODE_ITEM                     :    CodeItem,
	TYPE_STRING_DATA_ITEM              :    StringDataItem,
	TYPE_DEBUG_INFO_ITEM               :    DebugInfoItem,
	TYPE_ANNOTATION_ITEM               :    AnnotationItemItem,
	TYPE_ENCODED_ARRAY_ITEM            :    EncodedArrayItem,
	TYPE_ANNOTATIONS_DIRECTORY_ITEM    :    AnnotationsDirectoryItem,

}