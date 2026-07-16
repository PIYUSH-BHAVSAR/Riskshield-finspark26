import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const NetworkGraph = ({ graphData }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) return;

    const { nodes, edges } = graphData;

    // Clear previous SVG contents
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth || 600;
    const height = 500;

    // Set height attributes
    svg.attr('height', height);

    // Create a container group for zooming
    const container = svg.append('g');

    // Add Zoom behavior
    svg.call(
      d3.zoom()
        .scaleExtent([0.5, 3])
        .on('zoom', (event) => {
          container.attr('transform', event.transform);
        })
    );

    // Color definitions based on Node Type
    const getNodeColor = (type) => {
      switch (type) {
        case 'customer':
          return '#6366f1'; // Indigo
        case 'transaction':
          return '#f97316'; // Orange
        case 'security_event':
          return '#eab308'; // Amber
        case 'device':
          return '#ec4899'; // Hot Pink
        case 'ip':
          return '#06b6d4'; // Cyan
        case 'geo':
          return '#a855f7'; // Purple
        default:
          return '#94a3b8'; // Slate
      }
    };

    // Size definitions based on Node Type
    const getNodeSize = (type) => {
      switch (type) {
        case 'customer':
          return 24;
        case 'transaction':
        case 'security_event':
          return 18;
        default:
          return 12;
      }
    };

    // Deep copy nodes and edges to avoid D3 modifying React state directly
    const nodesCopy = nodes.map(d => ({ ...d }));
    const edgesCopy = edges.map(d => ({ ...d }));

    // Set up Force Simulation
    const simulation = d3.forceSimulation(nodesCopy)
      .force('link', d3.forceLink(edgesCopy).id(d => d.id).distance(130))
      .force('charge', d3.forceManyBody().strength(-350))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(d => getNodeSize(d.type) + 20));

    // Render Edges
    const link = container.append('g')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(edgesCopy)
      .join('line')
      .attr('stroke', (d) => d.type === 'correlation' ? '#ef4444' : '#334155')
      .attr('stroke-width', (d) => d.type === 'correlation' ? 3 : 1.5)
      .attr('class', (d) => d.type === 'correlation' ? 'correlation-line' : '');

    // Add arrow heads for correlation links
    svg.append('defs').append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 25)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#ef4444');

    d3.selectAll('.correlation-line').attr('marker-end', 'url(#arrow)');

    // Render Node Groups
    const node = container.append('g')
      .selectAll('g')
      .data(nodesCopy)
      .join('g')
      .call(
        d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    // Draw circles for nodes
    node.append('circle')
      .attr('r', d => getNodeSize(d.type))
      .attr('fill', d => getNodeColor(d.type))
      .attr('stroke', '#070a13')
      .attr('stroke-width', 2)
      .style('cursor', 'grab')
      .style('filter', d => d.type === 'customer' || d.type === 'transaction' ? `drop-shadow(0px 0px 8px ${getNodeColor(d.type)})` : 'none');

    // Add Node Labels
    node.append('text')
      .attr('dy', d => getNodeSize(d.type) + 16)
      .attr('text-anchor', 'middle')
      .text(d => d.label)
      .attr('fill', '#e2e8f0')
      .attr('font-size', '11px')
      .attr('font-weight', '500')
      .style('pointer-events', 'none')
      .style('text-shadow', '0 2px 4px rgba(0,0,0,0.8)');

    // Add Title Tooltips
    node.append('title')
      .text(d => `${d.label}\n\n${d.details || ''}`);

    // Update positions on each tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x}, ${d.y})`);
    });

    // Drag Helper Functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [graphData]);

  return (
    <div className="graph-container">
      <svg ref={svgRef} className="graph-svg"></svg>
    </div>
  );
};

export default NetworkGraph;
