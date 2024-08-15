define munki_item::item (
  $ensure = 'present',
  $catalog = 'production',
  $force_catalog_update = false
) {

  include munki_item

  munki_package { $name:
    ensure  => $ensure,
    catalog => $catalog,
    force_catalog_update => $force_catalog_update,
    require => File['/usr/local/munki/munki_do.py'],
  }
}
