<template>
  <b-row class="justify-content-center">
    <b-col cols="10">
      <div class="bar-chart">
        <h3>bar</h3>
        <div id="chart"></div>
      </div>
      <div class="scale">
        <h3>scale</h3>
        <span class="scale-num"></span>
        <div class="scale-icon-section"></div>

        <div id="scale-bar" class="scale-bar">
          <div class="scale-indicator"></div>
        </div>
      </div>
    </b-col>
  </b-row>
</template>
<script>
import * as d3 from "d3";
export default {
  name: "MyChart",
  data() {
    return {
      scale_active_idx: null,
      data: {
        user_basic: {
          age: 25,
          name: "John Doe",
          gender: "Male",
          date: "08-08-2023",
        },
        body_basic: {
          height: 180,
          weight: 75,
          visceral_fat: 15,
          metabolic: 1500,
        },
        body_comp: {
          r_arm: {
            FM: 5,
            LTM: 10,
            BMC: 1,
          },
          r_leg: {
            FM: 8,
            LTM: 12,
            BMC: 2,
          },
          l_arm: {
            FM: 4,
            LTM: 8,
            BMC: 1,
          },
          l_leg: {
            FM: 6,
            LTM: 10,
            BMC: 2,
          },
          trunk: {
            FM: 7,
            LTM: 15,
            BMC: 3,
          },
        },
      },
    };
  },
  mounted() {
    this.activateCharts();
  },
  methods: {
    activateCharts() {
      this.createBarChart();
      this.createScale();
    },
    createScale() {
      const data = [
        { level: "Level 1", range: [1, 10] },
        { level: "Level 2", range: [10, 30] },
        { level: "Level 3", range: [30, 40] },
        { level: "Level 4", range: [40, 50] },
        { level: "Level 5", range: [50, 100] },
      ];

      const margin = { top: 0, right: 10, bottom: 0, left: 10 };
      const width = 800 - margin.left - margin.right;
      const height = 50 - margin.top - margin.bottom;

      const svg = d3
        .select("#scale-bar")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top);

      const xScale = d3
        .scaleLinear()
        .domain([1, data[data.length - 1].range[1]])
        .range([0, width]);

      //   define the color scale
      const colorScale = d3
        .scaleLinear()
        .domain([0, data.length - 1])
        .range(["#E5F5F9", "#2CA25F"])
        .interpolate(d3.interpolateHcl);

      svg
        .append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(${margin.left}, ${margin.top + 20})`)
        .transition()
        .duration(1000)
        .call(d3.axisBottom(xScale));

      svg
        .selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", (d) => xScale(d.range[0]) + margin.left)
        .attr("width", (d) => xScale(d.range[1]) - xScale(d.range[0]))
        .attr("height", 20)
        .attr("fill", (d, i) => colorScale(i));

      // define icons
      const icons = d3
        .select(".scale-icon-section")
        .selectAll(".scale-icon")
        .data(data)
        .enter()
        .append("div")
        .attr("class", "scale-icon")
        .style("cursor", "pointer")
        .on("mouseover", function (d, i) {
          d3.select(`.scale rect:nth-child(${i + 2})`).attr(
            "fill",
            "rgba(15, 42, 22)"
          );
        })
        .on("mouseout", function () {
          d3.selectAll(`.scale rect`).attr("fill", (d, i) => colorScale(i));
        });

      icons
        .append("svg")
        .attr("width", 20)
        .attr("height", 20)
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 10)
        .attr("fill", (d, i) => colorScale(i));

      icons
        .append("span")
        .text((d) => `${d.level}: ${d.range[0]} - ${d.range[1]}`);

      //   const indicator = 3;
      d3.select(".scale-indicator")
        .append("svg")
        .attr("width", 20)
        .attr("height", 20)
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 10)
        .attr("fill", "black");

      const target = 80;

      d3.select(".scale-indicator").style(
        "transform",
        `translate(${target * 8 - margin.left - 5}px, ${-5}px)`
      );
    },
    createBarChart() {
      const data = [
        { label: "A", value: 10 },
        { label: "B", value: 20 },
        { label: "C", value: 15 },
        { label: "D", value: 8 },
        { label: "E", value: 12 },
      ];
      const width = 300;
      const height = 300;
      const margin = { top: 10, right: 10, bottom: 30, left: 40 };

      const svg = d3
        .select("#chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      const chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

      const xScale = d3
        .scaleBand()
        .range([0, width - margin.left - margin.right])
        .domain(data.map((d) => d.label))
        .padding(0.1);

      const yScale = d3
        .scaleLinear()
        .range([height - margin.top - margin.bottom, 0])
        .domain([0, d3.max(data, (d) => d.value)]);

      chart
        .append("g")
        .call(d3.axisBottom(xScale))
        .attr(
          "transform",
          `translate(0, ${height - margin.top - margin.bottom})`
        );

      chart.append("g").call(d3.axisLeft(yScale));

      const bars = chart
        .selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", (d) => xScale(d.label))
        .attr("y", (d) => yScale(d.value))
        .attr("width", xScale.bandwidth())
        .attr(
          "height",
          (d) => height - margin.top - margin.bottom - yScale(d.value)
        )
        .attr("fill", "steelblue");

      // Add tooltips
      const tooltip = d3
        .select("#chart")
        .append("div")
        .attr("class", "chart-tooltip")
        .style("opacity", 0);

      bars
        .on("mouseover", function (d) {
          d3.select(this).transition().duration(200).style("opacity", 0.8);
          tooltip
            .transition()
            .duration(200)
            .style("opacity", 1)
            .style("cursor", "pointer")
            .style("left", `${event.pageX - width / 2}px`)
            .style("top", `${event.pageY - 100}px`);
          console.log(event, d);
          tooltip.html(`Label: ${d.label}<br>Value: ${d.value}`);
        })
        .on("mouseout", function () {
          d3.select(this).transition().duration(200).style("opacity", 1);
          tooltip.transition().duration(500).style("opacity", 0);
        });
    },
  },
};
</script>
<style lang="scss">
.bar {
  fill: steelblue;
}
.chart-tooltip,
.scale-tooltip {
  position: absolute;
  background-color: #e7e7e7;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  opacity: 0;
}
.scale-icon-section {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 1rem;
}

.scale-icon {
  display: flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 1rem;
  border: 1px solid rgba(0, 100, 0, 0);
  span {
    padding-left: 10px;
  }
  &:hover {
    border: 1px solid darkgreen;
  }
}

.scale-bar {
  position: relative;
  .scale-indicator {
    position: absolute;
    circle {
      stroke: darkgreen;
      fill: white;
      filter: drop-shadow(4px 6px 1px rgb(5, 5, 5));
    }
  }
}

// .active {
//   border: 1px solid darkgreen;
// }
</style>
