import bpy

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nodes = mat.node_tree.nodes
    mixshader = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeMixShader)), None)
    transparent = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeBsdfTransparent)), None)
    light = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeLightPath)), 0)
    emission = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeEmission)), 0)
    image = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeTexImage)), None)
    output = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeOutputMaterial)), None)
    
    if mixshader is None or output is None:
        continue
    
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    
    l = image.outputs[0].links[0]
    mat.node_tree.links.remove(l)
    ll = image.outputs[1].links[0]
    mat.node_tree.links.remove(ll)
    
    lll = light.outputs[0].links[0]
    mat.node_tree.links.remove(lll)
    
    llll = emission.outputs[0].links[0]
    mat.node_tree.links.remove(llll)
    
    principled.location = (mixshader.location[0] - 100, mixshader.location[1])    
    
    mat.node_tree.links.new(image.outputs[0], principled.inputs[0])
    mat.node_tree.links.new(image.outputs[1], principled.inputs[21])
    
    mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    
    nodes.remove(mixshader)
    nodes.remove(transparent)
    nodes.remove(light)
    nodes.remove(emission)
    
try: 
    bpy.data.images['*'].filepath = 'C:/Blender/textures/*.png' 
except:
    pass