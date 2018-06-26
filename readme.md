# dim / coord / distort / fill

I am creating an animation pipeline. I call it "dim / coord / distort / fill". The principle is as follows.

## dimension
- dimension is the attribute generated on each point (or vertex or primitive)
- dimension is usually a static attribute, but can also be animated
- its values are 0-1 (for example, where the object should be revealed first, the dimensions are 0)
- this attribute is generated similarly to @uv, but it is meant to have a specific flow on the geometry:
 - linear falloff
 - radial falloff
 - geodesic falloff
 - along curvatures
 - noise patterns

## coordinate
- coordinate is one (detail) attribute for the whole object
- this attribute is meant to be animated
- its value is 0-1 
- the value is a "place" or altitude, or level of dimension
- at this place (or above/below) "something should happen" 
- it can be driven by MIDI

## fill
- fill is a general name of function that evaluates dimension versus coordinate
- it generates an "result attribute" which we later use to drive anything
- the principle is similar to filling the dimension up to the right coordinate
- also can be described as a search for places where the dimension is equal to the coordinate
- the function supports:
 - smooth feather
 - remapping of the falloff from the "hit"

## distort
- distort is powerful set of functions
- I used to adjust dimension or trace fill

### segment
- for example, on the human body we could segment the dimensions (hands, legs, hull)
- Mappi
- Segmentation

### bias
- Another way to adjust the resulting dimension or fill in space or time.

### ease
- Another way to adjust the resulting dimension or fill in space or time.

### noise
- Another way to adjust the resulting dimension or fill in space or time.

### lut
- Another way to adjust the resulting dimension or fill in space or time.

### shrink
- Another way to adjust the resulting dimension or fill in space or time.

## apply
- the resulting attribute can be used for any purpose:
- amount of particle generation
- temperature of the fire
- velocity field for flip
- strength of constraints
- primitive primitives, transformed packed primitives
