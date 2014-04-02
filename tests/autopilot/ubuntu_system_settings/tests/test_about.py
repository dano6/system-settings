# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2013 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

import os
import subprocess

from gi.repository import GLib

from autopilot.matchers import Eventually
from autopilot.platform import model
from testtools import skipIf
from testtools.matchers import Equals, NotEquals

from ubuntu_system_settings.tests import (
    AboutBaseTestCase,
    StorageBaseTestCase,
    LicenseBaseTestCase
)
from ubuntu_system_settings.utils.i18n import ugettext as _

import dbus


class AboutTestCase(AboutBaseTestCase):
    """ Tests for About this phone Page """

    def _get_imei_from_dbus(self):
        bus = dbus.SystemBus()
        manager = dbus.Interface(
            bus.get_object('org.ofono', '/'), 'org.ofono.Manager'
        )
        modems = manager.GetModems()

        for path, properties in modems:
            return properties['Serial']

    def _get_os_name(self):
        os_id = subprocess.check_output(['lsb_release', '-is'])
        os_release = subprocess.check_output(['lsb_release', '-rs'])

        return '{} {}'.format(os_id.strip(), os_release.strip())

    def _get_device_serial_number(self):
        return subprocess.check_output(['getprop', 'ro.serialno']).strip()

    def _get_device_manufacturer_and_model(self):
        manufacturer = subprocess.check_output(
            ['getprop', 'ro.product.manufacturer']
            ).strip()
        hw_model = subprocess.check_output(
            ['getprop', 'ro.product.model']
            ).strip()

        return '{} {}'.format(manufacturer, hw_model)

    def _get_system_image_iface(self):
        bus = dbus.SystemBus()
        service = bus.get_object('com.canonical.SystemImage', '/Service')
        iface = dbus.Interface(service, 'com.canonical.SystemImage')
        return iface.Info()

    def _get_last_updated_date(self):
        info = self._get_system_image_iface()[3]

        if info == 'Unknown':
            return _('Never')
        else:
            return str(info.split()[0])

    def test_serial(self):
        """Checks whether the UI is showing the correct serial number."""
        item = self.about_page.select_single(objectName='serialItem')

        if model() == 'Desktop':
            self.assertThat(item.visible, Equals(False))
        else:
            self.assertThat(
                item.value, Equals(self._get_device_serial_number())
            )

    def test_imei_information_is_correct(self):
        """Checks whether the UI is exposing the right IMEI."""
        imei_item = self.about_page.wait_select_single(
            objectName='imeiItem')

        if model() == 'Desktop':
            self.assertThat(imei_item.visible, Equals(False))
        else:
            self.assertEquals(imei_item.value, self._get_imei_from_dbus())

    def test_settings_show_correct_version_of_the_os(self):
        """Ensure the UI is showing the correct version of the OS."""
        item = self.about_page.select_single(objectName='osItem')
        # TODO: find a way to check the image build number as well
        # -- om26er 10-03-2014
        self.assertTrue(self._get_os_name() in item.value)

    @skipIf(subprocess.call(
        ['which', 'getprop'], stdout=subprocess.PIPE) != 0,
        'program "getprop" not found'
    )
    def test_hardware_name(self):
        """Ensure the UI is showing the correct device name."""
        device_label = self.about_page.select_single(
            objectName='deviceLabel'
            ).text
        device_name_from_getprop = self._get_device_manufacturer_and_model()

        self.assertEquals(device_label, device_name_from_getprop)

    def test_last_updated(self):
        """Checks whether Last Updated info is correct."""
        last_updated = self.about_page.select_single(
            objectName='lastUpdatedItem'
            ).value

        self.assertEquals(last_updated, self._get_last_updated_date())


class StorageTestCase(StorageBaseTestCase):
    """ Tests for Storage """

    def _get_space_by_directory(self, dir_name):
        if dir_name == 'Music':
            location = GLib.get_user_special_dir(
                GLib.UserDirectory.DIRECTORY_MUSIC
            )
        elif dir_name == 'Videos':
            location = GLib.get_user_special_dir(
                GLib.UserDirectory.DIRECTORY_VIDEOS
            )
        elif dir_name == 'Pictures':
            location = GLib.get_user_special_dir(
                GLib.UserDirectory.DIRECTORY_PICTURES
            )
        else:
            raise ValueError(
                '{} directory not handled by this fuction, you need to enhance'
                ' this function to handle that directory.'.format(dir_name)
            )

        if not os.path.exists(location):
            self.skipTest('glib directory {} does not exist'.format(dir_name))

        output = subprocess.check_output(['du', '--block-size=1', location])
        disk_space = output.split()[len(output.split()) - 2]
        return disk_space

    def test_disk(self):
        """ Checks whether disk item is available """
        disk_item = self.storage_page.wait_select_single(objectName='diskItem')
        self.assertThat(disk_item.text, Equals('Total storage'))

    def test_space(self):
        """ Checks whether storage item is available """
        self.assert_space_item('storageItem', _('Free space'))

    def test_space_ubuntu(self):
        """ Checks storage item """
        self.assert_space_item('usedByUbuntuItem', _('Used by Ubuntu'))

    def test_space_used_by_movies(self):
        """ Checks whether space shown to be used by movies is
        correct. """
        movie_space = self._get_space_by_directory('Videos')
        movie_space_in_ui = self.get_storage_space_used_by_category(
            'moviesItem'
        )

        self.assertThat(movie_space_in_ui, Eventually(Equals(movie_space)))

    def test_space_used_by_music(self):
        """ Checks whether space shown to be used by music is
        correct. """
        music_space = self._get_space_by_directory('Music')
        music_space_in_ui = self.get_storage_space_used_by_category(
            'audioItem'
        )

        self.assertThat(music_space_in_ui, Eventually(Equals(music_space)))

    def test_space_used_by_pictures(self):
        """ Checks whether space shown to be used by pictures is
        correct. """
        pictures_space = self._get_space_by_directory('Pictures')
        pictures_space_in_ui = self.get_storage_space_used_by_category(
            'picturesItem'
        )

        self.assertThat(
            pictures_space_in_ui, Eventually(Equals(pictures_space))
        )

    def test_space_other_files(self):
        """ Checks whether space item is available """
        self.assert_space_item('otherFilesItem', _('Other files'))

    def test_space_used_by_apps(self):
        """ Checks whether space item is available """
        self.assert_space_item('usedByAppsItem', _('Used by apps'))

    def test_installed_apps(self):
        """ Checks whether Installed Apps list is available """
        installed_apps_list_view = self.storage_page.select_single(
            objectName='installedAppsListView'
        )
        self.assertThat(installed_apps_list_view, NotEquals(None))


class LicenseTestCase(LicenseBaseTestCase):
    """ Tests for Licenses """

    def test_licenses_page(self):
        """ Check whether Storage page is available """
        self.assertThat(self.licenses_page.active, Eventually(Equals(True)))
