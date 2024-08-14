Puppet::Type.newtype(:munki_package) do
  desc 'This is a type that will use Munki to install a package:

    munki_package { \'Firefox\':
      ensure  => present,
      catalog => \'production\',
      }
  '

  ensurable

  newparam(:name, :namevar => true) do
    desc 'The package name as known to Munki'
  end
  newparam(:catalog) do
     desc 'The catalog from which we will get the package'
     defaultto 'production'
  end
end


