'use client'

import { useState, useEffect } from 'react'

interface DeviceInfo {
  isMobile: boolean
  hasCamera: boolean
  isIOS: boolean
  isAndroid: boolean
}

export function useDeviceDetection(): DeviceInfo {
  const [deviceInfo, setDeviceInfo] = useState<DeviceInfo>({
    isMobile: false,
    hasCamera: false,
    isIOS: false,
    isAndroid: false
  })

  useEffect(() => {
    const userAgent = navigator.userAgent.toLowerCase()
    const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent)
    const isIOS = /iphone|ipad|ipod/i.test(userAgent)
    const isAndroid = /android/i.test(userAgent)
    
    // Check for camera availability
    const hasCamera = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)

    setDeviceInfo({
      isMobile,
      hasCamera,
      isIOS,
      isAndroid
    })
  }, [])

  return deviceInfo
}