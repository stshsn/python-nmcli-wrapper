============================================
Python wrapper for NetworkManager-CLI(nmcli)
============================================

To manipulate network configuration from python code on Linux,
you can use this module as a wrapper to nmcli.

Requirements
============

* Python >= 3.7
* NetworkManager(nmcli)

How to Install
==============

> pip install python-nmcli-wrapper

Example
=======

Example code
.. code-block:: python
    from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS


    nm = NMCLI()

    returncode, stdout, stderr = nm.show_version()
    print(stdout, end="")
