# Puppet-munki_item Module

This module provides a defined type for managing items in a Munki repository. The item must be available to the device in the specified catalog for this to work. 

### Usage

```puppet


munki_item::item { 'Firefox':
  ensure  => 'present',
  catalog => 'production,
}
```

## Parameters

* `name`: The name of the item to manage (this is also the name variabke for the resource).
* `ensure`: Whether the item should be present or absent. Default: `present`.
* `catalog`: The catalog to which the item should be retrieved from. Default: `production`.

## To Do

* Add in some more checks to ensure Munki is present and configured before attempoting to install items.

## Credits

The `munki_do.py` script is graciously provided by [Greg Neagle](https://github.com/gregneagle).
