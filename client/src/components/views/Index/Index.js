// 세계 증시 현황

import React from 'react';
import { Table } from 'antd';

import indexes_kr from './data/indexes_kr.json'; // 지수 데이터

function Index() {
  const dataSource = indexes_kr;
  
  const columns = [
    {
      title: '지수',
      dataIndex: 'idxNm',
      key: 'idxNm',
    },
    {
      title: '시가',
      dataIndex: 'mkp',
      key: 'mkp',
    },
    {
      title: '고가',
      dataIndex: 'hipr',
      key: 'hipr',
    },
    {
      title: '저가',
      dataIndex: 'lopr',
      key: 'lopr',
    },
    {
      title: '종가',
      dataIndex: 'clpr',
      key: 'clpr',
    },
  ];
  

  return (
    <div>
      <a/>
        <Table dataSource={dataSource} columns={columns} />
    </div>
  )
}

export default Index