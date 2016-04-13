/*
 * This file is part of system-settings
 *
 * Copyright (C) 2013-2016 Canonical Ltd.
 *
 * Contact: Didier Roche <didier.roches@canonical.com>
 *          Diego Sarmentero <diego.sarmentero@canonical.com>
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 3, as published
 * by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranties of
 * MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QMenuModel 0.1
import QtQuick 2.4
import SystemSettings 1.0
import Ubuntu.Components 1.3
import Ubuntu.Components.ListItems 1.3 as ListItem
import Ubuntu.Components.Popups 1.3
import Ubuntu.OnlineAccounts.Client 0.1
import Ubuntu.SystemSettings.Update 1.0
import Ubuntu.Connectivity 1.0


ItemPage {
    id: root
    objectName: "systemUpdatesPage"

    // property bool isCharging: indicatorPower.deviceState === "charging"
    // property bool batterySafeForUpdate: isCharging || chargeLevel > 25
    // property var chargeLevel: indicatorPower.batteryLevel || 0

    // QDBusActionGroup {
    //     id: indicatorPower
    //     busType: 1
    //     busName: "com.canonical.indicator.power"
    //     objectPath: "/com/canonical/indicator/power"
    //     property variant batteryLevel: action("battery-level").state
    //     property variant deviceState: action("device-state").state
    //     Component.onCompleted: start()
    // }

    // Connections {
    //     id: networkingStatus
    //     target: NetworkingStatus
    //     onOnlineChanged: {
    //         if (NetworkingStatus.online) {
    //             // Set to searching, and start a search for updates
    //         } else {
    //             // Stop all things
    //         }
    //     }
    // }

    // Setup {
    //     id: uoaConfig
    //     applicationId: "ubuntu-system-settings"
    //     providerId: "ubuntuone"

    //     onFinished: {
    //         // Found credentials, do stuff that now can be done
    //     }
    // }

    Component {
         id: dialogErrorComponent
         Dialog {
             id: dialogueError
             title: i18n.tr("Installation failed")
             text: root.errorDialogText

             Button {
                 text: i18n.tr("OK")
                 color: UbuntuColors.orange
                 onClicked: {
                     PopupUtils.close(dialogueError);
                 }
             }
         }
    }

    Flickable {
        id: scrollWidget

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: configuration.top

        contentHeight: contentItem.childrenRect.height
        boundsBehavior: (contentHeight > root.height) ? Flickable.DragAndOvershootBounds : Flickable.StopAtBounds
        /* Set the direction to workaround https://bugreports.qt-project.org/browse/QTBUG-31905
           otherwise the UI might end up in a situation where scrolling doesn't work */
        flickableDirection: Flickable.VerticalFlick

        Updates {

        }
    }

    Column {
        id: configuration

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        ListItem.ThinDivider {}
        ListItem.SingleValue {
            objectName: "configuration"
            text: i18n.tr("Auto download")
            value: {
                if (UpdateManager.downloadMode === 0)
                    return i18n.tr("Never")
                else if (UpdateManager.downloadMode === 1)
                    return i18n.tr("On wi-fi")
                else if (UpdateManager.downloadMode === 2)
                    return i18n.tr("Always")
            }
            progression: true
            onClicked: pageStack.push(Qt.resolvedUrl("Configuration.qml"))
        }
    }
}
