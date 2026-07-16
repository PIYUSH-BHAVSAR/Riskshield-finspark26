import React from 'react';

const RiskBadge = ({ level }) => {
  const normalizedLevel = level ? level.toLowerCase() : 'low';
  return (
    <span className={`badge badge-${normalizedLevel}`}>
      {level || 'Low'}
    </span>
  );
};

export default RiskBadge;
