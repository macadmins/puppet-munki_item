class munki_item {
  file { '/usr/local/munki/munki_do.py':
    ensure => file,
    mode   => '0700',
    owner  => '0',
    group  => '0',
    source => 'puppet:///modules/munki_item/munki_do.py',
  }
}
