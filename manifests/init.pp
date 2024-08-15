class munki_item {
  file { '/usr/local/munki/munki_do.py':
    ensure => file,
    mode   => '0700',
    owner  => '0',
    group  => '0',
    source => 'puppet:///modules/munki_item/munki_do.py',
  }

  file { '/usr/local/munki/update_catalog.sh':
    ensure => file,
    mode   => '0700',
    owner  => '0',
    group  => '0',
    source => 'puppet:///modules/munki_item/update_catalog.sh',
  }

  exec { 'update_munki_catalog':
    command     => '/usr/local/munki/update_catalog.py',
    logoutput   => false,
    refreshonly => false,
    unless      => '/bin/true',
    require     => File['/usr/local/munki/update_catalog.py'],
  }
}
