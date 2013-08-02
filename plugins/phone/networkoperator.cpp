/*
 * Copyright (C) 2013 Canonical Ltd
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Ken VanDine <ken.vandine@canonical.com>
 *
*/

#include "networkoperator.h"

NetworkOperator::NetworkOperator(QObject *parent) :
    QObject(parent)
{
    m_ofonoNetworkRegistration = new OfonoNetworkRegistration(OfonoModem::AutomaticSelect, QString(), this);

    m_name = m_ofonoNetworkRegistration->name();
    qDebug() << "NAME: " << m_name;
    m_status = m_ofonoNetworkRegistration->status();
    qDebug() << "STATUS: " << m_status;
    m_technology = technologyToInt(m_ofonoNetworkRegistration->technology());
    qDebug() << "TECHNOLOGY: " << m_technology;
    QObject::connect(m_ofonoNetworkRegistration,
        SIGNAL (nameChanged (const QString&)),
        this,
        SLOT (operatorNameChanged(const QString&)));
    QObject::connect(m_ofonoNetworkRegistration,
        SIGNAL (statusChanged (const QString&)),
        this,
        SLOT (operatorStatusChanged(const QString&)));
    QObject::connect(m_ofonoNetworkRegistration,
        SIGNAL (technologyChanged (const QString&)),
        this,
        SLOT (operatorTechnologyChanged(const QString&)));
}

NetworkOperator::CellDataTechnology NetworkOperator::technologyToInt(const QString &technology)
{
    if (technology == QString(QStringLiteral("gprs")))
        return NetworkOperator::GprsDataTechnology;
    else if (technology == QString(QStringLiteral("edge")))
        return NetworkOperator::EdgeDataTechnology;
    else if (technology == QString(QStringLiteral("umts")))
        return NetworkOperator::UmtsDataTechnology;
    else if (technology == QString(QStringLiteral("hspa")))
        return NetworkOperator::HspaDataTechnology;

    return NetworkOperator::UnknownDataTechnology;
}

QString NetworkOperator::name() const
{
    return m_name;
}

void NetworkOperator::operatorNameChanged(const QString &name)
{
    m_name = name;
    qDebug() << "NAME: " << m_name;
    emit nameChanged(m_name);
}

QString NetworkOperator::status() const
{
    return m_status;
}

void NetworkOperator::operatorStatusChanged(const QString &status)
{
    m_status = status;
    qDebug() << "STATUS: " << m_status;
    emit statusChanged(m_status);
}
NetworkOperator::CellDataTechnology NetworkOperator::technology() const
{
    return m_technology;
}

void NetworkOperator::operatorTechnologyChanged(const QString &technology)
{
    m_technology = technologyToInt(technology);
    qDebug() << "TECHNOLOGY: " << m_technology;
    emit technologyChanged(m_technology);
}

NetworkOperator::~NetworkOperator()
{
}
