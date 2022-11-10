// 세계 증시 현황

import React from 'react';
import { Table } from 'antd';

import indexes_kr from './data/indexes_kr.json'; // 지수 데이터

function Index() {
  // const dataSource = indexes_kr;
  
  const columns = [
    {
      title: '지수명',
      dataIndex: 'index_name',
      key: 'index_name',
    },
    {
      title: '국가',
      dataIndex: 'nation',
      key: 'nation',
    },
    {
      title: '고가',
      dataIndex: 'high_price',
      key: 'high_price',
    },
    {
      title: '저가',
      dataIndex: 'low_price',
      key: 'low_price',
    },
    {
      title: '종가',
      dataIndex: 'close_price',
      key: 'close_price',
    },
    {
      title: '전일대비 등락률',
      dataIndex: 'fluctuation_rate',
      key: 'fluctuation_rate',
    },
  ];
  

  return (
    <div>
      <a/>
        <Table dataSource={indexes_kr} columns={columns} />
    </div>
  )
}

export default Index