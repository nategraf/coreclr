if(CLR_CMAKE_TARGET_TIZEN_LINUX)
  set(FEATURE_GDBJIT_LANGID_CS 1)
endif()

if(NOT DEFINED FEATURE_EVENT_TRACE)
  set(FEATURE_EVENT_TRACE 1)
endif(NOT DEFINED FEATURE_EVENT_TRACE)

if(NOT DEFINED FEATURE_PERFTRACING)
  set(FEATURE_PERFTRACING 1)
endif(NOT DEFINED FEATURE_PERFTRACING)

if(NOT DEFINED FEATURE_DBGIPC)
  if(CLR_CMAKE_PLATFORM_UNIX AND (NOT CLR_CMAKE_PLATFORM_ANDROID))
    set(FEATURE_DBGIPC 1)
  endif()
endif(NOT DEFINED FEATURE_DBGIPC)

if(NOT DEFINED FEATURE_INTERPRETER)
  set(FEATURE_INTERPRETER 0)
endif(NOT DEFINED FEATURE_INTERPRETER)
if(NOT WIN32)
  if(NOT DEFINED FEATURE_NI_BIND_FALLBACK)
    if(NOT CLR_CMAKE_TARGET_ARCH_AMD64 AND NOT CLR_CMAKE_TARGET_ARCH_ARM64)
      set(FEATURE_NI_BIND_FALLBACK 1)
    endif()
  endif(NOT DEFINED FEATURE_NI_BIND_FALLBACK)
endif(NOT WIN32)

if(NOT DEFINED FEATURE_APPDOMAIN_RESOURCE_MONITORING)
  set(FEATURE_APPDOMAIN_RESOURCE_MONITORING 1)
endif(NOT DEFINED FEATURE_APPDOMAIN_RESOURCE_MONITORING)

if(NOT DEFINED FEATURE_STANDALONE_GC)
  set(FEATURE_STANDALONE_GC 1)
endif(NOT DEFINED FEATURE_STANDALONE_GC)
