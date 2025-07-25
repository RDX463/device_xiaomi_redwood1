#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/redwood',
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/qcom-caf/sm8350',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.xiaomi.hardware.misys@1.0',
        'vendor.xiaomi.hardware.misys@2.0',
        'vendor.xiaomi.hardware.misys@3.0',
        'vendor.xiaomi.hardware.misys@4.0',
        'vendor.xiaomi.hardware.displayfeature@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/etc/media_lahaina/video_system_specs.json', 'vendor/etc/media_yupik_v1/video_system_specs.json'): blob_fixup()
        .regex_replace('"max_retry_alloc_output_timeout": 10000,', '"max_retry_alloc_output_timeout": 0,'),
    'vendor/etc/vintf/manifest/c2_manifest_vendor.xml': blob_fixup()
        .regex_replace('.*ozoaudio.*\n?', '')
        .regex_replace('.*dolby.*\n?', ''),
    ('vendor/etc/init/android.hardware.drm@1.3-service.widevine.rc', 'vendor/etc/init/vendor.qti.media.c2@1.0-service.rc'): blob_fixup()
        .regex_replace('writepid /dev/cpuset/foreground/tasks', 'task_profiles ProcessCapacityHigh'),
    ('vendor/etc/init/android.hardware.neuralnetworks@1.3-service-qti.rc'): blob_fixup()
        .regex_replace('writepid /dev/stune/nnapi-hal/tasks', 'task_profiles NNApiHALPerformance'),
    'vendor/etc/public.libraries.txt': blob_fixup()
        .regex_replace('.*libqti-perfd-client.so.*\n?', ''),
    'vendor/lib64/android.hardware.secure_element@1.0-impl.so': blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
    ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
         .add_needed('libcrypto_shim.so'),
    ('vendor/etc/camera/pureShot_parameter.xml', 'vendor/etc/camera/pureView_parameter.xml'): blob_fixup()
        .regex_replace(r'=(\d+)>', r'="\1">'),
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .binary_regex_replace(b'\x73\x74\x5F\x6C\x69\x63\x65\x6E\x73\x65\x2E\x6C\x69\x63', b'\x63\x61\x6D\x65\x72\x61\x5F\x63\x6E\x66\x2E\x74\x78\x74')
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/hw/camera.xiaomi.so': blob_fixup()
        .sig_replace('29 07 00 94', '1F 20 03 D5'),
    'vendor/lib64/hw/com.qti.chi.override.so' : blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/libmialgo_rfs.so': blob_fixup()
        .clear_symbol_version('remote_handle64_close')
        .clear_symbol_version('remote_handle64_invoke')
        .clear_symbol_version('remote_handle64_open')
        .clear_symbol_version('remote_register_buf_attr')
        .clear_symbol_version('remote_session_control'),
    ('vendor/lib64/libalAILDC.so', 'vendor/lib64/libalLDC.so', 'vendor/lib64/libalhLDC.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/libarcsoft_hdrplus_hvx_stub.so': blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open'),
    'vendor/lib64/libsensor_cal_v2.so': blob_fixup()
        .add_needed('libjsoncpp_shim.so'),
    'vendor/lib64/hw/displayfeature.default.so': blob_fixup()
        .replace_needed('vendor.xiaomi.hardware.displayfeature@1.0.so', 'vendor.xiaomi.hardware.displayfeature@1.0_vendor.so'),
    ('vendor/etc/media_codecs.xml', 'vendor/etc/media_codecs_yupik_v0.xml', 'vendor/etc/media_codecs_yupik_v1.xml'): blob_fixup()
        .regex_replace('.+media_codecs_(google_audio|google_c2|google_telephony|vendor_audio).+\n', ''),
}  # fmt: skip

module = ExtractUtilsModule(
    'redwood',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
