import QtQuick 2.0
import Ubuntu.Components 0.1
import Ubuntu.Components.ListItems 0.1 as ListItem

Column {
    anchors {
        left: parent.left
        right: parent.right
    }
    spacing: units.gu(1)

    property string category
    property string categoryName

    ListItem.Header {
        text: categoryName
    }

    Grid {
        anchors.left: parent.left
        anchors.right: parent.right
        columns: width / units.gu(14)

        Repeater {
            model: pluginManager.itemModel(category)

            delegate: Loader {
                id: loader
                width: units.gu(14)
                sourceComponent: model.item.entryComponent

                Connections {
                    ignoreUnknownSignals: true
                    target: loader.item
                    onClicked: {
                        var pageComponent = model.item.pageComponent
                        if (pageComponent) {
                            pageStack.push(model.item.pageComponent,
                                           { plugin: model.item })
                        }
                    }
                }
            }
        }
    }
    ListItem.ThinDivider {}
}
