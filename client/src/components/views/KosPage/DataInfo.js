import React from "react";
import { Table } from 'antd';
import financials_kr from './data/financials_kr.json';

function DataInfo(props) {
  const dataSource = financials_kr;

  const columns = [
    {
      title: '시장 구분',
      dataIndex: 'mrktCtg',
      key: 'mrktCtg',
    },
    {
      title: '종목명',
      dataIndex: 'itmsNm',
      key: 'itmsNm',
    },
    {
      title: '기업 홈페이지',
      dataIndex: 'enpHmpgUrl',
      key: 'enpHmpgUrl',
    },
    {
      title: '시가',
      dataIndex: '9610',
      key: '9610',
    },
    {
      title: '종가',
      dataIndex: 'clpr',
      key: 'clpr',
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
    }
  ];

  return (
    <div>
      <a/>
        <Table dataSource={dataSource} columns={columns} />
    </div>
  );
}

export default DataInfo;