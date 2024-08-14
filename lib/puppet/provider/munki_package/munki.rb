Puppet::Type.type(:munki_package).provide(:munki) do
  desc "Manages a package in Munki"

  commands :munki_do => '/usr/local/munki/munki_do.py'

  def exists?
    system "/usr/local/munki/munki_do.py --checkstate #{resource[:name]} --catalog #{resource[:catalog]}"
  end

  def create
    unless munki_do('--install', resource[:name], '--catalog', resource[:catalog])
      raise Puppet::Error, "Failed to install #{resource[:name]}"
    end
  end

  def destroy
    unless munki_do('--uninstall', resource[:name], '--catalog', resource[:catalog])
      raise Puppet::Error, "Failed to uninstall #{resource[:name]}"
    end
  end
end
