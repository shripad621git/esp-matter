# spiffs_create_partition_image
#
# Create a spiffs image of the specified directory on the host during build and optionally
# have the created image flashed using `idf.py flash`
function(factory_partition_create_image partition esp_matter_dir)
    set(options FLASH_IN_PROJECT)
    set(multi DEPENDS)
    cmake_parse_arguments(arg "${options}" "" "${multi}" "${ARGN}")
    get_filename_component(esp_matter_dir_full_path ${esp_matter_dir} ABSOLUTE)

    set(mfg_tool_py ${PYTHON} ${esp_matter_dir}/tools/mfg_tool/mfg_tool.py)

    partition_table_get_partition_info(size "--partition-name ${partition}" "size")
    partition_table_get_partition_info(offset "--partition-name ${partition}" "offset")

    if("${size}" AND "${offset}")
        set(MY_BULB_NAME "My bulb")
        set(VENDOR_ID 0xFFF2)
        set(PRODUCT_ID 0x8001)
        set(KEY_FILE_PATH "${esp_matter_dir_full_path}/connectedhomeip/connectedhomeip/credentials/test/attestation/Chip-Test-PAI-FFF2-8001-Key.pem")
        set(CERT_FILE_PATH "${esp_matter_dir_full_path}/connectedhomeip/connectedhomeip/credentials/test/attestation/Chip-Test-PAI-FFF2-8001-Cert.pem")
        set(PASSCODE 20202020)
        set(DISCRIMINATOR 3841)

        # Execute Factory partition image generation; this always executes as there is no way to specify for CMake to watch for
        # contents of the base dir changing.
        execute_process(
            COMMAND ${mfg_tool_py} -cn "${MY_BULB_NAME}"
                                   -v ${VENDOR_ID}
                                   -p ${PRODUCT_ID}
                                   --pai -k ${KEY_FILE_PATH} -c ${CERT_FILE_PATH}
                                   --passcode ${PASSCODE}
                                   --discriminator ${DISCRIMINATOR}
                                   OUTPUT_VARIABLE MFG_TOOL_OUTPUT
                                   OUTPUT_STRIP_TRAILING_WHITESPACE
                                   )
        message(STATUS "MFG_TOOL_OUTPUT : ${MFG_TOOL_OUTPUT}")     
        string(REGEX MATCH "Generated output files at:/s (.+)" GENERATED_FILES_PATH "${MFG_TOOL_OUTPUT}")
        string(REGEX MATCH "([^/]+)$" GENERATED_FILES_DIRECTORY "${GENERATED_FILES_PATH}")

        message(STATUS "Generated Files Path: ${GENERATED_FILES_PATH}")

        set(image_file "${CMAKE_BINARY_DIR}/${GENERATED_FILES_PATH}/${GENERATED_FILES_DIRECTORY}-partition.bin")
        add_custom_target(factory_${partition}_bin
              COMMAND ${CMAKE_COMMAND} -E echo "Image File: ${image_file}"
         )

        set_property(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}" APPEND PROPERTY
            ADDITIONAL_MAKE_CLEAN_FILES
            ${image_file})

        idf_component_get_property(main_args esptool_py FLASH_ARGS)
        idf_component_get_property(sub_args esptool_py FLASH_SUB_ARGS)
        # Last (optional) parameter is the encryption for the target. In our
        # case, spiffs is not encrypt so pass FALSE to the function.
        esptool_py_flash_target(${partition}-flash "${main_args}" "${sub_args}" ALWAYS_PLAINTEXT)
        esptool_py_flash_to_partition(${partition}-flash "${partition}" "${image_file}")

        add_dependencies(${partition}-flash factory_${partition}_bin)

        if(arg_FLASH_IN_PROJECT)
            esptool_py_flash_to_partition(flash "${partition}" "${image_file}")
            add_dependencies(flash factory_${partition}_bin)
        endif()
    else()
        set(message "Failed to create Factory partition image for partition '${partition}'. "
                    "Check project configuration if using the correct partition table file.")
        fail_at_build_time(factory_${partition}_bin "${message}")
    endif()
endfunction()
