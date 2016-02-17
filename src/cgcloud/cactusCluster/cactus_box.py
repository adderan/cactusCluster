from cgcloud.toil.toil_box import ToilLatestBox
from cgcloud.core.cluster import ClusterLeader, ClusterWorker
from cgcloud.fabric.operations import sudo, run
from cgcloud.core.box import fabric_task

class CactusBox( ToilLatestBox ):
    def _list_packages_to_install( self ):
        return super( CactusBox, self)._list_packages_to_install() + ['git', 'g++', 'python-dev']

    @fabric_task
    def __fix_python( self ):
        sudo( 'ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/' )

    @fabric_task
    def __install_cactus( self ):
        run( 'git clone http://github.com/adderan/progressiveCactus/' )
        run( 'cd progressiveCactus && git checkout toil' )
        run( 'cd progressiveCactus && git submodule update --init' )
        run( 'cd progressiveCactus && make clusterNode' )
        
    def _post_install_packages( self ):
        super( CactusBox, self)._post_install_packages()
        self.__fix_python()
        self.__install_cactus()

class CactusLeader( CactusBox, ClusterLeader):
    pass

class CactusWorker( CactusBox, ClusterWorker ):
    pass
