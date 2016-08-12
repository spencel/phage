import QtQuick 2.5
import QtQuick.Window 2.2

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    MainForm {
        color: "#eef5f6"
        border.color: "#00000000"
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent

        MouseArea {
            id: exitProgramButton
            x: 23
            y: 433
            width: 93
            height: 39
            onClicked: {
                Qt.quit();
            }

            Text {
                id: exitProgramButtonText
                x: 35
                y: 17
                text: qsTr("Exit")
                font.pixelSize: 12
            }
        }

        Rectangle {
            id: allGbkToJson
            x: 8
            y: 8
            width: 624
            height: 30
            color: "#ffffff"
            border.width: 1

            TextInput {
                id: allGbktoJsonInput
                x: 0
                y: 0
                width: 524
                height: 30
                text: qsTr("type in the path of the folder containing gbk files")
                cursorVisible: true
                inputMask: qsTr("")
                font.pixelSize: 12
            }

            Rectangle {
                id: allGbktoJsonButton
                x: 524
                y: 0
                width: 100
                height: 30
                color: "#ffffff"
                border.color: "#000000"

                MouseArea {
                    id: allGbktoJsonButtonMouseArea
                    x: 0
                    y: 0
                    width: 260
                    height: 150
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.top: parent.top
                    anchors.left: parent.left
                    hoverEnabled: true
                    onClicked: {

                    }

                }

                Text {
                    id: allGbktoJsonButtonText
                    x: 0
                    y: 0
                    width: 260
                    height: 150
                    text: qsTr("Generate JSON")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.top: parent.top
                    anchors.left: parent.left
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 12
                }
            }
        }
    }
}
