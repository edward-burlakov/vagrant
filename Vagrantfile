Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-20.04"
        config.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = "2"
        config.vm.network "forwarded_port", guest: 19999, host: 19999
    #    vb.customize ["modifyvm", :id, "--memory", ENV['ram_memory_size_mb']]
    #    vb.customize ["modifyvm", :id, "--cpus", ENV['cpu_count']]
        end
end