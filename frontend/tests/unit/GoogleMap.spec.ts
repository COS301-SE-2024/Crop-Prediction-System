// @vitest-environment nuxt

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import GoogleMap from '~/components/GoogleMap.vue'

// Mock Google Maps
globalThis.google = {
  maps: {
    Map: class {
      constructor(container, options) {
        this.container = container
        this.options = options
      }
    },
    drawing: {
      DrawingManager: class {
        constructor(options) {
          this.options = options
        }
        setMap(map) {
          this.map = map
        }
        setDrawingMode(mode) {
          this.drawingMode = mode
        }
      },
      OverlayType: {
        POLYGON: 'polygon',
      },
    },
    Polygon: class {
      constructor(options) {
        this.options = options
      }
      setMap(map) {
        this.map = map
      }
      getPath() {
        return {
          getArray() {
            return [
              { lat: () => 1, lng: () => 1 }
            ]
          }
        }
      }
    },
    ControlPosition: {
      TOP_CENTER: 'top_center',
    },
    event: {
      addListener() {},
      clearListeners() {},
    },
  },
}

describe('GoogleMap', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(GoogleMap, {
      global: {
        mocks: {
          $mapsLoader: {
            load: vi.fn().mockResolvedValue(true),
          },
        },
      },
    })
  })

  it('should mount the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('should set drawing mode', async () => {
    const drawingManager = {
      setDrawingMode: vi.fn(),
    }
    wrapper.vm.drawingManager = drawingManager

    // Call setDrawingMode with `true`
    wrapper.vm.setDrawingMode(true)

    expect(drawingManager.setDrawingMode).toHaveBeenCalledWith('polygon')
  })

  it('should get polygon paths', async () => {
    const polygon = {
      getPath() {
        return {
          getArray() {
            return [{ lat: () => 1, lng: () => 1 }]
          }
        }
      }
    }
    wrapper.vm.polygons = [polygon]

    const paths = wrapper.vm.getPolygonPaths()

    expect(paths).toEqual([[[1, 1]]])
  })
})
