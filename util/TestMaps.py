"""
This example demonstrates the animation of multiple icons
on a map using TrackingViz objects.
"""

from osmviz.animation import SimViz, TrackingViz, Simulation
import pygame

## The goal is to show 10 trains racing eastward across the US.

right_lon = 4.9677
left_lon = 4.7933
top_lat = 45.7848
bottom_lat = 45.7153

begin_time = 0
end_time = 10

image_f = "./pt.png"
zoom=14
red = pygame.Color("red")

class LassoViz(SimViz):
  """
  LassoViz draws a line between two (optionally moving) locations.
  """

  def __init__(self, getLocAtTime1, getLocAtTime2,
               linecolor=red, linewidth=3,
               drawingOrder=0):
    """
    getLocAtTime 1 and 2 represent the location of the 1st and 2nd
    endpoint of this lasso, respectively. They should take a single 
    argument (time) and return the (lat,lon) of that endpoint.
    """
    SimViz.__init__(self, drawingOrder);
    self.xy1 = None
    self.xy2 = None
    self.linecolor = linecolor
    self.linewidth = linewidth
    self.getLoc1 = getLocAtTime1
    self.getLoc2 = getLocAtTime2

  def setState(self, simtime, getXY):
    self.xy1 = getXY(*self.getLoc1(simtime))
    self.xy2 = getXY(*self.getLoc2(simtime))

  def drawToSurface(self, surf):
    pygame.draw.line(surf, self.linecolor, self.xy1, self.xy2,
                     self.linewidth)

  ## So long as we are passing LassoViz's in as part of the scene_viz
  ## list to a Simulation, we don't need to implement the getLabel,
  ## getBoundingBox, or mouseIntersect methods.


trackvizs = []

def makeInterpolator(lat, lon):
  def ret(t):
      return (lat, lon)
  return ret

lat = bottom_lat+ 1 * (top_lat-bottom_lat)

locAtTime1 = makeInterpolator(45.7270459, 4.8653198)
locAtTime2 = makeInterpolator(45.7238159, 4.8694674)

tviz = TrackingViz( "Client 1", image_f, locAtTime1,
                   (begin_time,end_time),
                   (bottom_lat, top_lat, left_lon, right_lon),
                   1)
tviz2 = TrackingViz( "Client 2", image_f, locAtTime2,
                   (begin_time,end_time),
                   (bottom_lat, top_lat, left_lon, right_lon),
                   1) #drawing order doesn't really matter here

trackvizs.append(tviz)
trackvizs.append(tviz2)

lasso = LassoViz(locAtTime1,
                 locAtTime2)
sim = Simulation( trackvizs, [lasso,], 0 )
sim.run(speed=1,refresh_rate=10,osmzoom=zoom)