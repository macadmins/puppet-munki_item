Puppet::Type.type(:munki_package).provide(:munki) do
  desc "Manages a package in Munki"

  commands :munki_do => '/usr/local/munki/munki_do.py'

  def exists?
    return false if force_install == true
    system "/usr/local/munki/munki_do.py --checkstate #{resource[:name]} --catalog #{resource[:catalog]}"
    exit_code = $?.exitstatus
    if exit_code == 0
      return true
    elsif exit_code == 1
      return false
    elsif exit_code == 2
      raise Puppet::Error, "Failed to check state of #{resource[:name]} - package not found"
    else
      raise Puppet::Error, "Failed to check state of #{resource[:name]} - exit code #{exit_code}"
    end
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
