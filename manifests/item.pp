define munki_item::item (
  $ensure = 'present',
  $catalog = 'production',
) {

  include munki_item

  munki_package { $name:
    ensure  => $ensure,
    catalog => $catalog,
    require => [File['/usr/local/munki/munki_do.py'], Exec['update_munki_catalog']],
  }
}
