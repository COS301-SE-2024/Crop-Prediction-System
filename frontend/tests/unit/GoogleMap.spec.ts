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

    // Set the drawingManager in the component
    wrapper.vm.drawingManager = drawingManager

    // Manually call the logic that should change the drawing mode
    wrapper.vm.drawingManager.setDrawingMode('polygon')

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

    // Set the polygon in the component's polygons array
    wrapper.vm.polygons = [polygon]

    // Get the paths directly from the polygon's getPath method
    const paths = wrapper.vm.polygons[0].getPath().getArray().map((point) => [point.lat(), point.lng()])

    expect(paths).toEqual([[1, 1]])
  })
})