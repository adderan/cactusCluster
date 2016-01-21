from cgcloud.toil.toil_cluster import ToilCluster
from cgcloud.cactusCluster.cactus_box import CactusLeader, CactusWorker


class CactusCluster( ToilCluster ):
    @property
    def worker_role( self ):
        return CactusWorker

    @property
    def leader_role( self ):
        return CactusLeader
