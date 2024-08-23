define munki_item::item (
  $ensure = 'present',
  $catalog = 'production'
  $force_install = false
) {

  include munki_item

  munki_package { $name:
    ensure  => $ensure,
    catalog => $catalog,
    require => File['/usr/local/munki/munki_do.py'],
    notify  => Exec['run_munki'],
  }
}
