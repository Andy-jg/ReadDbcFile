#!/usr/bin/python
################################################################################
# Grey 2016.03.02
# Update : add the function to gnerate M script for data import.
# Grey  2016.03.01
# generate variables list according to dbc file.
# Inupt : dbc file name as a string, excel file name as a string.
# Output : An excel file : variables list file
# jiajia do the test and up to git 
# I read the Web http://blog.sina.com.cn/s/blog_627927570102w8cd.html
import re
from xlwt import Workbook
def GetVarList(dbc_file,var_list,model_name):
    data_c_file       = model_name + '_Data.c'
    data_head_file    = model_name + '_Data.h'
    fid               = open('var_import.m','w')
    book              = Workbook()
    sheet_result      = book.add_sheet('variables')
    data_type_dict    = {2:'uint8',8:'uint8',12:'uint16',16:'uint16'}
    text_lines        = open(dbc_file,'r')
    regexp_var        = re.compile(r'SG_\s+(\w+)\s+.*\|(\w+)@')
    var_detail        = re.compile(r'SG_.*\((\S+),(\S+)\).*\[(\S+)\|(\S+)\].*\"(\S*)\"')
    index_col_num     = 0
    var_name_col_num  = 1
    data_type_col_num = 2
    raw_num           = 0
    sheet_result.write(raw_num,index_col_num,'index')
    sheet_result.write(raw_num,var_name_col_num,'variable name')
    sheet_result.write(raw_num,data_type_col_num,'data type')
    for each_line in text_lines:
        line_info  = each_line.strip()
        if line_info.startswith('SG_ '):
            search_result     = regexp_var.search(line_info)
            var_detail_result = var_detail.search(line_info)
            try:
                raw_num += 1
                var_name      = search_result.group(1)
                data_index    = int(search_result.group(2))
                data_type     = data_type_dict[data_index]
                factor_value  = var_detail_result.group(1)
                bias_value    = var_detail_result.group(2)
                min_value     = var_detail_result.group(3)
                max_value     = var_detail_result.group(4)
                unit_str      = var_detail_result.group(5)
                sheet_result.write(raw_num,index_col_num,raw_num)
                sheet_result.write(raw_num,var_name_col_num,var_name)
                sheet_result.write(raw_num,data_type_col_num,data_type)
                if data_type   == 'uint8':
                    fid.write("%s = copy(base_8bit);\n" % var_name)
                    fid.write("%s.DataType = \'fixdt(0,8,%s,%s)\';\n" %(var_name,factor_value,bias_value))
                    fid.write("%s.Min = %s;\n" % (var_name,0))
                    fid.write("%s.Max = %s;\n" % (var_name,255))
                    fid.write("%s.DocUnits = \'%s\';\n" % (var_name,unit_str))
                    fid.write("%s.RTWInfo.CustomAttributes.DefinitionFile = '%s';\n" % (var_name,data_c_file))
                    fid.write("%s.RTWInfo.CustomAttributes.HeaderFile = '%s';\n" % (var_name,data_head_file))
                elif data_type == 'uint16':
                    fid.write("%s = copy(base_16bit);\n" % var_name)
                    fid.write("%s.DataType = \'fixdt(0,16,%s,%s)\';\n" %(var_name,factor_value,bias_value))
                    fid.write("%s.Min = %s;\n" % (var_name,0))
                    fid.write("%s.Max = %s;\n" % (var_name,65535))
                    fid.write("%s.DocUnits = \'%s\';\n" % (var_name,unit_str))
                    fid.write("%s.RTWInfo.CustomAttributes.DefinitionFile = '%s';\n" % (var_name,data_c_file))
                    fid.write("%s.RTWInfo.CustomAttributes.HeaderFile = '%s';\n" % (var_name,data_head_file))
                    #print("%s factor : %s\t bias : %s\tMin : %s\tMax : %s\tUnit : %s" % \
                    #(var_name,factor_value,bias_value,min_value,max_value,unit_str))
            except:
                print("ERROR:%s" % line_info)
    book.save(var_list)
    fid.close()
    print("Process Done! Please refer to excel file %s" % var_list)
GetVarList('test.dbc','temp.xls','DbcTst')
