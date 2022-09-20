import React from 'react';
import stockData from './data/financials_kr.json';
import { Link } from 'react-router-dom';
import { Table } from 'antd';

// function Card({stock}) {
  

const Card = () => {
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
      title: '종목코드',
      dataIndex: 'shotnIsin',
      key: 'shotnIsin',
    },
    {
      title: '법인명',
      dataIndex: 'corpNm',
      key: 'corpNm',
    },
    {
      title: '법인 홈페이지',
      dataIndex: 'enpHmpgUrl',
      key: 'enpHmpgUrl',
    },
    {
      title: '법인 전화번호',
      dataIndex: 'enpTlno',
      key: 'enpTlno',
    },
    {
      title: '액면가',
      dataIndex: 'stckParPrc',
      key: 'stckParPrc',
    },
    {
      title: '전일 대비 등락',
      dataIndex: 'vs',
      key: 'vs',
    },
    {
      title: '전일 대비 등락율',
      dataIndex: 'fltRt',
      key: 'fltRt',
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
      title: '거래량',
      dataIndex: 'trqu',
      key: 'trqu',
    },
  ];
  const stocks = stockData.map(stock => {
    return (
      <div key={stock.id}>
        <Link to={`detail/${stock.id}`}>
          <Table dataSource={stockData} columns={columns} />
        </Link>
      </div>
    );
    });



  return (
    <>
    {stocks}
    </>
  );
};

export default Card;
