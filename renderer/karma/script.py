import hou
import sys
from pxr import Usd, Sdf

#print("Script arguments", sys.argv)

maxDepth = 15

settings = stage.GetPrimAtPath("/Render/RenderSettings")
print(settings)

attr = settings.CreateAttribute("karma:global:samplesperpixel", Sdf.ValueTypeNames.Int)
attr.Set(int(32))

attr = settings.CreateAttribute("karma:global:colorlimit", Sdf.ValueTypeNames.Float)
attr.Set(float(800))
attr = settings.CreateAttribute("karma:global:colorlimitindirect", Sdf.ValueTypeNames.Float)
attr.Set(float(800))

attr = settings.CreateAttribute("karma:global:convergence_mode", Sdf.ValueTypeNames.Int)
attr.Set(int(0))


attr = settings.CreateAttribute("karma:object:diffuselimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))
attr = settings.CreateAttribute("karma:global:diffuselimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))

attr = settings.CreateAttribute("karma:object:volumelimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))
attr = settings.CreateAttribute("karma:global:volumelimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))

attr = settings.CreateAttribute("karma:object:reflectlimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))
attr = settings.CreateAttribute("karma:global:reflectlimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))

attr = settings.CreateAttribute("karma:object:refractlimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))
attr = settings.CreateAttribute("karma:global:refractlimit", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))

attr = settings.CreateAttribute("karma:global:russianroulette_cutoff", Sdf.ValueTypeNames.Int)
attr.Set(int(maxDepth))


