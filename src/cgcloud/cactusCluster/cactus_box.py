from cgcloud.toil.toil_box import ToilLatestBox
from cgcloud.core.cluster import ClusterLeader, ClusterWorker
from cgcloud.fabric.operations import sudo, run
from cgcloud.core.box import fabric_task
from cgcloud.lib.util import heredoc
from cgcloud.mesos.mesos_box import work_dir, mesos_service, user
import os

class CactusBox( ToilLatestBox ):
    def _list_packages_to_install( self ):
        return super( CactusBox, self)._list_packages_to_install() + ['git', 'g++', 'python-dev']

    @fabric_task
    def __fix_python( self ):
        sudo( 'ln -s /usr/lib/python2.7/plat-*/_sysconfigdata_nd.py /usr/lib/python2.7/' )

    @fabric_task ( user="mesosbox" )
    def __install_cactus( self ):
        progressiveCactusDir = os.path.join(self._shared_dir(), "progressiveCactus")
        run( 'git clone http://github.com/adderan/progressiveCactus %s' % progressiveCactusDir )
        run( 'cd %s && git checkout toil' % progressiveCactusDir )
        run( 'cd %s && git submodule update --init' % progressiveCactusDir)
        run( 'cd %s && make clusterNode' % progressiveCactusDir)

    @fabric_task
    def __start_mesos_node_on_master( self ):
        service = mesos_service( 'slave',
                           '--master=mesos-master:5050',
                           '--no-switch_user',
                           '--work_dir=' + work_dir,
                           '$(cat /var/lib/mesos/slave_args)' )
        start_on = "mesosbox-start-master"
        self._register_init_script(
                    service.init_name,
                    heredoc( """
                        description "{service.description}"
                        console log
                        start on {start_on}
                        stop on runlevel [016]
                        respawn
                        umask 022
                        limit nofile 8000 8192
                        setuid {user}
                        setgid {user}
                        env USER={user}
                        exec {service.command}""" ) )

    def _toil_pip_args( self ):
        return [ '--pre', 'toil[aws,mesos,encryption]' ]
        
    def _post_install_packages( self ):
        super( CactusBox, self)._post_install_packages()
        self.__fix_python()
        self.__install_cactus()

    def _post_install_mesos( self ):
        self.__start_mesos_node_on_master()
        super( CactusBox, self)._post_install_mesos()

class CactusLeader( CactusBox, ClusterLeader):
    pass

class CactusWorker( CactusBox, ClusterWorker ):
    pass
