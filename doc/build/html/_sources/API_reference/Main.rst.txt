.. _Main_API:

Main
====

.. py:module:: Main 

Script responsible for turning on the app and containing classes responsible for running simulations, managing queue, and functional GUI. 

Main script can be found at the root folder of entire AutoFluent.

.. py:class:: SimulationClass(simGeneralObject, simMeshObjectList,simTunnelObject,simSolverSett, simBoundarySett, simPostproSett, simParametersSett, simName)
        
    Class responsible for running each stage of simulation. 

    The initial parametres for this class are individual simulation settings from which the **SimulationClass** 
    runs the individual simulation steps.

    Attributes:

    .. py:attribute:: simGeneralObject
        :type: GeneralSett
    .. py:attribute:: simMeshObjectList
        :type: Dict(List(MeshObjects.Vehicle))
    .. py:attribute:: simTunnelObject
        :type: TunnelSett
    .. py:attribute:: simSolverSett
        :type: SimulationSett
    .. py:attribute:: simBoundarySett
        :type: Boundary_conditions_sett
    .. py:attribute:: simPostproSett
        :type: PostprocessSett
    .. py:attribute:: simParametersSett
        :type: ParametrizationSett

    .. py:attribute:: simName
        :type: String

    .. py:attribute:: SimID
        :type: Int

    .. py:attribute:: _registry
        :type: List(SimulationClass)

    .. py:attribute:: SimStat
        :type: String

    .. py:attribute:: meshPath
        :type: String

    .. py:attribute:: SimThread
        :type: String

    .. py:attribute:: solverPath
        :type: String

    .. py:method:: findSimID()