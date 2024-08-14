Puppet::Type.type(:munki_package).provide(:munki) do
  desc "Manages a package in Munki"

  commands :munki_do => '/usr/local/munki/munki_do.py'

  def exists?
    system "/usr/local/munki/munki_do.py --checkstate #{resource[:name]} --catalog #{resource[:catalog]}"
  end

  def create
    munki_do('--install', resource[:name], '--catalog', resource[:catalog])
  end

  def destroy
    munki_do('--uninstall', resource[:name], '--catalog', resource[:catalog])
  end
end
