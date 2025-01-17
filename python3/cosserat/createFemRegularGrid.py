# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""Basic scene using Cosserat in SofaPython3.

Based on the work done with SofaPython. See POEMapping.py
"""

__authors__ = "younesssss"
__contact__ = "adagolodjo@protonmail.com, yinoussa.adagolodjo@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2021,Inria"
__date__ = "March 16 2021"

def createFemCube(parentNode):
    FemNode = parentNode.addChild("FemNode")
    FemNode.addObject('VisualStyle', displayFlags='showBehaviorModels hideCollisionModels hideBoundingCollisionModels '
                                                  'showForceFields hideInteractionForceFields showWireframe')
    gelVolume = FemNode.addChild("gelVolume")
    gelVolume.addObject("RegularGridTopology", name="HexaTop", n="6 6 6", min="40 -16 -10", max="100 20 10")
    gelVolume.addObject("TetrahedronSetTopologyContainer", name="Container", position="@HexaTop.position")
    gelVolume.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    gelVolume.addObject("Hexa2TetraTopologicalMapping", input="@HexaTop", output="@Container", swapping="false")

    GelSurface = FemNode.addChild("GelSurface")
    GelSurface.addObject("TriangleSetTopologyContainer", name="Container", position="@../GelVolume/HexaTop.position")
    # GelSurface.addObject("TriangleSetTopologyModifier", input="@../GelVolume/Container", output="@Container",
    #                      flipNormals="false")

    gelNode = FemNode.addChild("gelNode")
    # gelNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels '
    #                                                  'hideMappings hideForceFields showWireframe '
    #                                                  'showInteractionForceFields hideForceFields')
    gelNode.addObject("EulerImplicitSolver", rayleighMass="0.1", rayleighStiffness="0.1")
    gelNode.addObject('SparseLDLSolver', name='preconditioner')
    gelNode.addObject('TetrahedronSetTopologyContainer', src="@../gelVolume/Container", name='container')
    # gelNode.addObject('TetrahedronSetTopologyModifier')
    gelNode.addObject('MechanicalObject', name='tetras', template='Vec3d')
    gelNode.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large',
                      poissonRatio='0.45', youngModulus='100')
    # gelNode.addObject('UniformMass', totalMass='5')
    gelNode.addObject('BoxROI', name='ROI1', box='40 -17 -10 100 -14 10', drawBoxes='true')
    gelNode.addObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness='1e12')

    surfaceNode = gelNode.addChild("surfaceNode")
    surfaceNode.addObject('TriangleSetTopologyContainer', name="surfContainer", src="@../../GelSurface/Container")
    surfaceNode.addObject('MechanicalObject', name='msSurface')
    surfaceNode.addObject('TriangleCollisionModel', name='surface')
    surfaceNode.addObject('BarycentricMapping')

    gelNode.addObject('LinearSolverConstraintCorrection')

    return FemNode
