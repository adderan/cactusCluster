def roles( ):
    from cgcloud.cactusCluster.cactus_box import (CactusBox, CactusLeader, CactusWorker)
    return sorted( locals( ).values( ), key=lambda cls: cls.__name__ )


def cluster_types( ):
    from cgcloud.cactusCluster.cactus_cluster import CactusCluster
    return sorted( locals( ).values( ), key=lambda cls: cls.__name__ )
