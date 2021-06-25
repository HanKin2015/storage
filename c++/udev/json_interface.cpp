/*
 * json_interface.cpp
 * json文件处理接口
 * 
 * date  : 2021.06.25
 * author: hankin
 * 
 * Copyright (c) 2021 hankin. All rights reserved.
 *
 */

#include "json_interface.hpp"

/*
 * @brief 将json文件内容解析成cjson对象
 * @param [IN]	json_file_path  json文件路径
 */
cJSON* GetJsonObject(const char* json_file_path)
{
    // 1.创建cjson对象
    cJSON* json_obj = cJSON_CreateObject();
    if (json_obj == nullptr) {
      printf("cJSON_CreateObject failed!\n");
      return nullptr;
    }
    
    // 2.读取json文件内容
    fstream fs(json_file_path); // 创建个文件流对象, 并打开文件
    stringstream ss;            // 创建字符串流对象
    ss << fs.rdbuf();           // 把文件流中的字符输入到字符串流中
    string content = ss.str();  // 获取流中的字符串内容
    
    // 3.解析字符串为json对象
    json_obj = cJSON_Parse(content.c_str());
    if (json_obj == nullptr) {
        printf("cJSON_Parse failed!\n");
        return nullptr;
    }

#if 1
    // 4.打印json对象内容
    char* json_cont = cJSON_Print(json_obj);
    printf("json_cont:\n%s\n", json_cont);

    // 5.获取json对象大小
    int json_array_size = cJSON_GetArraySize(json_obj);
    printf("json_array_size: %d\n", json_array_size);
#endif

    return json_obj;
}

string PrintCjsonType(cJSON* json_obj)
{
    switch (json_obj->type) {
    case cJSON_Number: return "cJSON_Number";
    case cJSON_String: return "cJSON_String";
    case cJSON_Array : return "cJSON_Array";
    case cJSON_Object: return "cJSON_Object";
    case cJSON_Raw   : return "cJSON_Raw";
    default          : return "other";
    }
}

/*
 * @brief 递归输出json对象的值
 * @param [IN]	json_file_path  json文件路径
 */
void PrintJsonValue(cJSON* json_obj)
{
    cJSON* iter1 = nullptr;  // 迭代器
    cJSON_ArrayForEach(iter1, json_obj) {
        if (iter1->type == cJSON_Array) {
            PrintJsonValue(iter1);
        } else if (iter1->type == cJSON_Object) {
            cJSON* iter2 = nullptr;
            cJSON_ArrayForEach(iter2, iter1) {
                char *key = nullptr, *value = nullptr;
                
                key = iter2->string;
                if (iter2->type == cJSON_Number) {  // 坑点,int和double如何去区分
                    printf("valueint: %d, valuedouble: %lf\n", iter2->valueint, iter2->valuedouble);
                    itoa(iter2->valueint, value, 16);
                } else if (iter2->type == cJSON_String || iter2->type == cJSON_Raw) {
                    value = iter2->valuestring;
                }

                printf("key: %s, value: %s\n", key, value);
            }
        } else {
            printf("type: %s\n", PrintCjsonType(iter1));
        }
    }
}