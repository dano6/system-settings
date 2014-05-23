/*
 * Copyright (C) 2014 Canonical, Ltd.
 *
 * Authors:
 *    Jussi Pakkanen <jussi.pakkanen@canonical.com>
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 3, as published
 * by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "previousnetworkmodel.h"
#include<QVariant>

PreviousNetworkModel::PreviousNetworkModel(QObject *parent) : QAbstractListModel(parent) {

}

int PreviousNetworkModel::rowCount(const QModelIndex &parent) const {
    return 0;
}


QVariant PreviousNetworkModel::data(const QModelIndex & index, int role) const {
    return QVariant();
}
