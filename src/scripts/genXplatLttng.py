##
## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.
##
##  Sample LTTng Instrumentation code that is generated:
##
## HEADER:
## #define GCFinalizersEnd_TRACEPOINT_ARGS \
##TP_ARGS(\
##        const unsigned int ,Count\
##)
##TRACEPOINT_EVENT_CLASS(
##    DotNETRuntime,
##    GCFinalizersEnd,
##    GCFinalizersEnd_TRACEPOINT_ARGS,
##     TP_FIELDS(
##        ctf_integer(unsigned int, Count, Count)
##    )
##)
##
##CPP :
##
##extern "C" BOOL  EventXplatEnabledGCFinalizersEnd(){ return TRUE;}
##extern "C" ULONG  FireEtXplatGCFinalizersEnd(
##                  const unsigned int Count
##)
##{
##  ULONG Error = ERROR_WRITE_FAULT;
##    if (!EventXplatEnabledGCFinalizersEnd()){ return ERROR_SUCCESS;}
##
##
##     tracepoint(
##        DotNETRuntime,
##        GCFinalizersEnd,
##        Count
##        );
##        Error = ERROR_SUCCESS;
##
##return Error;
##}
##
###define GCFinalizersEndT_TRACEPOINT_INSTANCE(name) \
##TRACEPOINT_EVENT_INSTANCE(\
##    DotNETRuntime,\
##    GCFinalizersEnd,\
##    name ,\
##    GCFinalizersEnd_TRACEPOINT_ARGS \
##)
#

import os 
from genXplatEventing import * 

stdprolog="""
//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.
//

/******************************************************************

DO NOT MODIFY. AUTOGENERATED FILE.
This file is generated using the logic from <root>/src/scripts/genXplatLttng.py

******************************************************************/
"""
stdprolog_cmake="""
#
#
#******************************************************************

#DO NOT MODIFY. AUTOGENERATED FILE.
#This file is generated using the logic from <root>/src/scripts/genXplatLttng.py

#******************************************************************
"""

lttngDataTypeMapping ={
        #constructed types
        "win:null"          :" ",
        "win:Int64"         :"const __int64",
        "win:ULong"         :"const ULONG",
        "win:count"         :"*",
        "win:Struct"        :"const int",
        #actual spec
        "win:GUID"          :"const int",
        "win:AnsiString"    :"const char*",
        "win:UnicodeString" :"const char*",
        "win:Double"        :"const double",
        "win:Int32"         :"const signed int",
        "win:Boolean"       :"const BOOL",
        "win:UInt64"        :"const unsigned __int64",
        "win:UInt32"        :"const unsigned int",
        "win:UInt16"        :"const unsigned short",
        "win:UInt8"         :"const unsigned char",
        "win:Pointer"       :"const size_t",
        "win:Binary"        :"const BYTE"
        }

ctfDataTypeMapping ={
        #constructed types
        "win:Int64"         :"ctf_integer",
        "win:ULong"         :"ctf_integer",
        "win:count"         :"ctf_sequence",
        "win:Struct"        :"ctf_sequence",
        #actual spec
        "win:GUID"          :"ctf_sequence",
        "win:AnsiString"    :"ctf_string",
        "win:UnicodeString" :"ctf_string",
        "win:Double"        :"ctf_float",
        "win:Int32"         :"ctf_integer",
        "win:Boolean"       :"ctf_integer",
        "win:UInt64"        :"ctf_integer",
        "win:UInt32"        :"ctf_integer",
        "win:UInt16"        :"ctf_integer",
        "win:UInt8"         :"ctf_integer",  #actually a character
        "win:Pointer"       :"ctf_integer",
        "win:Binary"        :"ctf_sequence"
        }

def generateLttngHeader(providerName,allTemplates,eventNodes):
    lTTngHdr = []    
    for templateName in allTemplates.keys():
        for subTemplate in allTemplates[templateName].allAbstractTemplateTypes:
            fnSig   = allTemplates[templateName].getFnFrame(subTemplate)
#TP_ARGS                
            tp_args       = []
            tp_args_param = []
            tp_args.append("\n#define ")
            tp_args.append(subTemplate)
            tp_args.append('_TRACEPOINT_ARGS \\\n')
            tp_args.append('TP_ARGS(\\\n')


            for params in fnSig.paramlist:
                fnparam     = fnSig.getParam(params)
                wintypeName = fnparam.winType
                typewName   = lttngDataTypeMapping[wintypeName]
                winCount    = fnparam.count
                countw      = lttngDataTypeMapping[winCount]
                
                tp_args_param.append("        ")
                tp_args_param.append(typewName)
                if countw != " ":
                    tp_args_param.append(countw)
                    
                tp_args_param.append(" ,")
                tp_args_param.append(fnparam.name)
                tp_args_param.append(",\\\n")
                
            if len(tp_args_param) > 0:
                del tp_args_param[-1]
            tp_args.extend(tp_args_param)
            tp_args.append("\\\n)\n")
            lTTngHdr.extend(tp_args)
#TP_EVENT_CLASS
            tp_fields =[]
            tp_fields.append("TRACEPOINT_EVENT_CLASS(\n")
            tp_fields.append("    " + providerName + ",\n")
            tp_fields.append("    " + subTemplate + ",\n")
            tp_fields.append("    " + subTemplate + "_TRACEPOINT_ARGS,\n")
            tp_fields.append("    " + " TP_FIELDS(\n")
#TP_FIELDS
                
            for params in fnSig.paramlist:
                fnparam     = fnSig.getParam(params)
                wintypeName = fnparam.winType
                typewName   = lttngDataTypeMapping[wintypeName]
                winCount    = fnparam.count
                countw      = lttngDataTypeMapping[winCount]
                typewName   = typewName.replace("const ","")

                tp_fields_body = []
                ctf_type       = None
                varname        = fnparam.name

                if fnparam.prop:
                    #this is an explicit struct treat as a sequence
                    ctf_type = "ctf_sequence"
                    sizeofseq = fnparam.prop
                    tp_fields_body.append(typewName + ", " + varname +", " +  varname + ",size_t,")
                    tp_fields_body.append(sizeofseq)

                else:
                    ctf_type = ctfDataTypeMapping[wintypeName]
                    if ctf_type == "ctf_string":
                        tp_fields_body.append(varname + ", " + varname)
                    elif ctf_type == "ctf_integer" or ctf_type == "ctf_float":
                        tp_fields_body.append(typewName + ", " + varname +", " +  varname)
                    elif ctf_type == "ctf_sequence":
                        raise Exception("ctf_sequence needs to have its memory expilicitly laid out")
                    else:
                        raise Exception("no such ctf intrinsic called: " +  ctf_type)


                tp_fields.append("        ")
                tp_fields.append(ctf_type + "(")
                tp_fields.extend(tp_fields_body)
                tp_fields.append(")\n")
                
            tp_fields.append("    )\n)\n")
            lTTngHdr.extend(tp_fields)

# Macro for defining event instance
            lTTngHdr.append("\n#define " + subTemplate)
            lTTngHdr.append("""T_TRACEPOINT_INSTANCE(name) \\
TRACEPOINT_EVENT_INSTANCE(\\
""")
            lTTngHdr.append("    "+providerName + ",\\\n")
            lTTngHdr.append("    " + subTemplate + ",\\\n")
            lTTngHdr.append("    name ,\\\n")
            lTTngHdr.append("    " + subTemplate + "_TRACEPOINT_ARGS \\\n)")

#add an empty template node to just specify the event name in the event stream
    lTTngHdr.append("\n\nTRACEPOINT_EVENT_CLASS(\n")
    lTTngHdr.append("    " +providerName + ",\n")
    lTTngHdr.append("    emptyTemplate ,\n")
    lTTngHdr.append("""    TP_ARGS(),
    TP_FIELDS()
)
#define T_TRACEPOINT_INSTANCE(name) \\
TRACEPOINT_EVENT_INSTANCE(\\
""")
    lTTngHdr.append("    " +providerName + ",\\\n")
    lTTngHdr.append("    emptyTemplate,\\\n")

    lTTngHdr.append("""    name ,\\
    TP_ARGS()\\
)""")
#end of empty template
# create the event instance in headers
    lTTngHdr.append("\n")
    for eventNode in eventNodes:
        eventName    = eventNode.getAttribute('symbol');
        templateName = eventNode.getAttribute('template');

        if not eventName :
            raise Exception(eventNode + " event does not have a symbol")
        if not templateName:
            lTTngHdr.append("T_TRACEPOINT_INSTANCE(")
            lTTngHdr.append(eventName +")\n")
            continue
            
        for subtemplate in allTemplates[templateName].allAbstractTemplateTypes:
            subevent = subtemplate;
            subevent = subevent.replace(templateName,'')
            lTTngHdr.append(subtemplate)
            lTTngHdr.append("T_TRACEPOINT_INSTANCE(")
            lTTngHdr.append(eventName + subevent + ")\n")

    lTTngHdr.append("\n#endif /* LTTNG_CORECLR_H")
    lTTngHdr.append(providerName + " */\n")
    lTTngHdr.append("#include <lttng/tracepoint-event.h>")

    return ''.join(lTTngHdr)
        
def generateLttngTpProvider(providerName,eventNodes,allTemplates):
    lTTngImpl = []
    for eventNode in eventNodes:
        eventName    = eventNode.getAttribute('symbol')
        templateName = eventNode.getAttribute('template')
        vars_to_be_freed = [] #vars representing the allocation we make
        #generate EventXplatEnabled
        lTTngImpl.append("extern \"C\" BOOL  EventXplatEnabled")
        lTTngImpl.append(eventName)
        lTTngImpl.append("(){ return TRUE;}\n")
        #generate FireEtw functions
        fnptype = []
        linefnptype = []
        fnptype.append("extern \"C\" ULONG  FireEtXplat")
        fnptype.append(eventName)
        fnptype.append("(\n")
        

        if templateName:
            for subtemplate in allTemplates[templateName].allAbstractTemplateTypes:
                fnSig   = allTemplates[templateName].getFnFrame(subtemplate)
                for params in fnSig.paramlist:
                    fnparam     = fnSig.getParam(params)
                    wintypeName = fnparam.winType
                    typewName   = palDataTypeMapping[wintypeName]
                    winCount    = fnparam.count
                    countw      = palDataTypeMapping[winCount]
                    
                    linefnptype.append(lindent)
                    linefnptype.append(typewName)
                    if countw != " ":
                        linefnptype.append(countw)
                        
                    linefnptype.append(" ")
                    linefnptype.append(fnparam.name)
                    linefnptype.append(",\n")

            if len(linefnptype) > 0 :
                del linefnptype[-1]

        fnptype.extend(linefnptype)
        fnptype.append("\n)\n")
        fnptype.append("{\n  ULONG Error = ERROR_WRITE_FAULT;\n")
        lTTngImpl.extend(fnptype)

#start of fn body
        lTTngImpl.append("    if (!EventXplatEnabled")
        lTTngImpl.append(eventName)
        lTTngImpl.append("()){ return ERROR_SUCCESS;}\n")

        linefnbody = []
        if templateName:
            #emit code to init variables convert unicode to ansi string            
            for subtemplate in allTemplates[templateName].allAbstractTemplateTypes:
                fnSig   = allTemplates[templateName].getFnFrame(subtemplate)
                for params in fnSig.paramlist:
                    fnparam     = fnSig.getParam(params)
                    wintypeName = fnparam.winType
                    paramname   = fnparam.name

                    if wintypeName == "win:UnicodeString":
                        lTTngImpl.append("    INT " + paramname + "_path_size = -1;\n")
                        lTTngImpl.append("    INT " + paramname + "_full_name_path_size")
                        lTTngImpl.append(" = WideCharToMultiByte( CP_ACP, 0, " + paramname + ", -1, NULL, 0, NULL, NULL );\n")
                        lTTngImpl.append("    CHAR* " + paramname + "_full_name = NULL;\n")
            
            lTTngImpl.append("\n")

#emit tracepoints
            for subtemplate in allTemplates[templateName].allAbstractTemplateTypes:
                fnSig   = allTemplates[templateName].getFnFrame(subtemplate)

                subevent   = subtemplate
                subevent   = subevent.replace(templateName,'')
                linefnbody.append("\n     tracepoint(\n")
                linefnbody.append("        " + providerName + ",\n")
                linefnbody.append("        " + eventName + subevent)
                linefnbody.append(",\n")

                for params in fnSig.paramlist:
                    fnparam     = fnSig.getParam(params)
                    wintypeName = fnparam.winType
                    winCount    = fnparam.count
                    paramname   = fnparam.name
                    ctf_type    = ctfDataTypeMapping.get(winCount)

                    linefnbody.append("        ")
                    if not ctf_type:
                        ctf_type    = ctfDataTypeMapping[wintypeName]

                    if ctf_type == "ctf_string" and wintypeName == "win:UnicodeString":
                        #emit code to convert unicode to ansi string
                        lTTngImpl.append("    "+ paramname + "_full_name = (CHAR*)malloc(")
                        lTTngImpl.append(paramname + "_full_name_path_size*sizeof(CHAR));\n")
                        
                        lTTngImpl.append("    _ASSERTE("+paramname+ "_full_name != NULL);\n")
                        lTTngImpl.append("    if(" + paramname + "_full_name == NULL){goto LExit;}\n\n")

                        lTTngImpl.append("    " + paramname+ "_path_size = WideCharToMultiByte( CP_ACP, 0, ")
                        lTTngImpl.append(paramname + ", -1, ")
                        lTTngImpl.append(paramname + "_full_name, ")
                        lTTngImpl.append(paramname + "_full_name_path_size, NULL, NULL );\n")
                        
                        lTTngImpl.append("    _ASSERTE(" +paramname+ "_path_size == " )
                        lTTngImpl.append(paramname + "_full_name_path_size );\n")
                        
                        lTTngImpl.append("    if( " + paramname + "_path_size == 0 ){ Error = ERROR_INVALID_PARAMETER; goto LExit;}\n")
                        
                        vars_to_be_freed.append(paramname + "_full_name")
                        
                        linefnbody.append(paramname + "_full_name")
                        linefnbody.append(",\n")
                        continue
                    
                    elif ctf_type == "ctf_sequence" or wintypeName == "win:Pointer":
                        linefnbody.append("(" + lttngDataTypeMapping[wintypeName])
                        if not  lttngDataTypeMapping[winCount] == " ":
                            linefnbody.append( lttngDataTypeMapping[winCount])
                            
                        linefnbody.append(") ")
                    
                    linefnbody.append(paramname)
                    linefnbody.append(",\n")
           
                if len(linefnbody) > 0 :
                    del linefnbody[-1]
                linefnbody.append("\n        );\n")
        
        else:
            linefnbody.append("\n     tracepoint(\n")
            linefnbody.append("        "+providerName + ",\n")
            linefnbody.append("        "+eventName)
            linefnbody.append("\n     );\n")
            
        lTTngImpl.extend(linefnbody)
        lTTngImpl.append("        Error = ERROR_SUCCESS;\n")

        if len(vars_to_be_freed) > 0:
            lTTngImpl.append("LExit:\n")
            vars_to_be_freed.reverse()
            for var in vars_to_be_freed:
                lTTngImpl.append("        if ("+ var + " != NULL) {free(" )
                lTTngImpl.append(var)
                lTTngImpl.append(");}\n")
                
        lTTngImpl.append("\nreturn Error;\n}\n")

    return ''.join(lTTngImpl)

def generateLttngFiles(etwmanifest,intermediate):

    tree           = DOM.parse(etwmanifest)

    if not os.path.exists(intermediate):
        os.makedirs(intermediate)
   
    eventprovider_directory      = intermediate + "/eventprovider/" 
    tracepointprovider_directory = eventprovider_directory + "/tracepointprovider"
    lttng_directory              = eventprovider_directory + "/lttng/"
    lttngevntprovPre             = lttng_directory + "/eventprov"
    lttngevntprovTpPre           = lttng_directory + "/traceptprov"

    if not os.path.exists(eventprovider_directory):
        os.makedirs(eventprovider_directory)
        
    if not os.path.exists(lttng_directory):
        os.makedirs(lttng_directory)
    
    if not os.path.exists(tracepointprovider_directory):
        os.makedirs(tracepointprovider_directory)


#Top level Cmake
    topCmake          = open(eventprovider_directory + "/CMakeLists.txt", 'w')
    topCmake.write(stdprolog_cmake + "\n")
    topCmake.write("""cmake_minimum_required(VERSION 2.8.12.2)

    project(eventprovider)

    set(CMAKE_INCLUDE_CURRENT_DIR ON)

    add_definitions(-DPAL_STDCPP_COMPAT=1)
    include_directories(${COREPAL_SOURCE_DIR}/inc/rt)
    include_directories(lttng)

    add_library(eventprovider
        STATIC
""")

    for providerNode in tree.getElementsByTagName('provider'):
        providerName = providerNode.getAttribute('name')
        providerName = providerName.replace("Windows-",'')
        providerName = providerName.replace("Microsoft-",'')

        providerName_File = providerName.replace('-','')
        providerName_File = providerName_File.lower()
        
        topCmake.write('        "'+ lttngevntprovPre + providerName_File + ".cpp" + '"\n')

    topCmake.write(""")
    add_subdirectory(tracepointprovider)
    
    # Install the static eventprovider library 
    install (TARGETS eventprovider DESTINATION lib)
    """)
    topCmake.close()

#TracepointProvider  Cmake
    
    tracepointprovider_Cmake          = open(tracepointprovider_directory + "/CMakeLists.txt", 'w')
    
    tracepointprovider_Cmake.write(stdprolog_cmake + "\n")
    tracepointprovider_Cmake.write("""cmake_minimum_required(VERSION 2.8.12.2)
    
    project(coreclrtraceptprovider)
    
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
    
    add_definitions(-DPAL_STDCPP_COMPAT=1)
    include_directories(${COREPAL_SOURCE_DIR}/inc/rt)
    include_directories(../lttng/)
    add_compile_options(-fPIC)
    
    add_library(coreclrtraceptprovider
        SHARED
    """)
    
    for providerNode in tree.getElementsByTagName('provider'):
        providerName = providerNode.getAttribute('name')
        providerName = providerName.replace("Windows-",'')
        providerName = providerName.replace("Microsoft-",'')

        providerName_File = providerName.replace('-','')
        providerName_File = providerName_File.lower()
        
        tracepointprovider_Cmake.write('        "'+ lttngevntprovTpPre + providerName_File +".cpp" + '"\n')

    tracepointprovider_Cmake.write("""    )
    
    target_link_libraries(coreclrtraceptprovider
                         -llttng-ust
    )
            
   #Install the static coreclrtraceptprovider library
   install (TARGETS coreclrtraceptprovider DESTINATION .)
   """)
    tracepointprovider_Cmake.close()

# Generate Lttng specific instrumentation
    for providerNode in tree.getElementsByTagName('provider'):
        
        providerName = providerNode.getAttribute('name')
        providerName = providerName.replace("Windows-",'')
        providerName = providerName.replace("Microsoft-",'')

        providerName_File = providerName.replace('-','')
        providerName_File = providerName_File.lower()
        providerName      = providerName.replace('-','_')

        lttngevntheadershortname = "tp" + providerName_File +".h";
        lttngevntheader          = eventprovider_directory +"lttng/"+ lttngevntheadershortname
        lttngevntprov            = lttngevntprovPre + providerName_File + ".cpp"
        lttngevntprovTp          = lttngevntprovTpPre + providerName_File +".cpp"


        lTTngHdr          = open(lttngevntheader, 'w')
        lTTngImpl         = open(lttngevntprov, 'w')
        lTTngTpImpl       = open(lttngevntprovTp, 'w')

        lTTngHdr.write(stdprolog + "\n")
        lTTngImpl.write(stdprolog + "\n")
        lTTngTpImpl.write(stdprolog + "\n")

        lTTngTpImpl.write("\n#define TRACEPOINT_CREATE_PROBES\n")
        
       
        lTTngTpImpl.write("#include \"./"+lttngevntheadershortname + "\"\n")
        
        lTTngHdr.write("""
#include "palrt.h"
#include "pal.h"

#undef TRACEPOINT_PROVIDER

""")


        lTTngHdr.write("#define TRACEPOINT_PROVIDER " + providerName + "\n")
        lTTngHdr.write("""

#undef TRACEPOINT_INCLUDE
""")

        lTTngHdr.write("#define TRACEPOINT_INCLUDE \"./" + lttngevntheadershortname + "\"\n\n")


        lTTngHdr.write("#if !defined(LTTNG_CORECLR_H" + providerName + ") || defined(TRACEPOINT_HEADER_MULTI_READ)\n\n")
        lTTngHdr.write("#define LTTNG_CORECLR_H" + providerName + "\n")

        lTTngHdr.write("\n#include <lttng/tracepoint.h>\n\n")

        lTTngImpl.write("""
#define TRACEPOINT_DEFINE
#define TRACEPOINT_PROBE_DYNAMIC_LINKAGE
""")
        lTTngImpl.write("#include \"" + lttngevntheadershortname + "\"\n\n")
        


        templateNodes = providerNode.getElementsByTagName('template')
        eventNodes = providerNode.getElementsByTagName('event')

        allTemplates  = parseTemplateNodes(templateNodes)
        #generate the header
        lTTngHdr.write(generateLttngHeader(providerName,allTemplates,eventNodes) + "\n")

        #create the implementation of eventing functions : lttngeventprov*.cp
        lTTngImpl.write(generateLttngTpProvider(providerName,eventNodes,allTemplates) + "\n")
        
        lTTngHdr.close()
        lTTngImpl.close()
        lTTngTpImpl.close()

import argparse
import sys

def main(argv):

    #parse the command line
    parser = argparse.ArgumentParser(description="Generates the Code required to instrument LTTtng logging mechanism")

    required = parser.add_argument_group('required arguments')
    required.add_argument('--man',  type=str, required=True,
                                    help='full path to manifest containig the description of events')
    required.add_argument('--intermediate', type=str, required=True,
                                    help='full path to intermediate directory')
    args, unknown = parser.parse_known_args(argv)
    if unknown:
        print('Unknown argument(s): ', ', '.join(unknown))
        return const.UnknownArguments

    sClrEtwAllMan     = args.man
    intermediate      = args.intermediate

    generateLttngFiles(sClrEtwAllMan,intermediate)

if __name__ == '__main__':
    return_code = main(sys.argv[1:])
    sys.exit(return_code)

