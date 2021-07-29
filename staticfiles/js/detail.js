function hotspot_graph(color, group, data) {
    const layers = d3.stack()
        .keys(group)
        .offset(d3.stackOffsetDiverging)
        (data);

    const tooltip = d3.select('body').append('div')
        .style('background', 'rgba(0, 0, 0, 0.9)')
        .style('color', 'white')
        .style('position', 'absolute')
        .style('z-index', '10')
        .style('visibility', 'hidden')
        .style('fill', '#000000')
        .attr('width', self.width + 10)
        .attr('height', self.height + 20);

    const svg = d3.select('svg'),
        margin = {
            top: 20,
            right: 30,
            bottom: 60,
            left: 0
        },
        width = +svg.attr('width'),
        height = +svg.attr('height');

    const x = d3.scaleLinear().rangeRound([margin.left, width - margin.right]);
    x.domain([d3.min(layers, stackMin), d3.max(layers, stackMax)]);

    const y = d3.scaleBand()
        .rangeRound([height - margin.bottom, margin.top])
        .padding(0.1);
    y.domain(data.map(function () {
        return 1;
    }))

    function stackMin(layers) {
        return d3.min(layers, function (d) {
            return d[0];
        });
    }

    function stackMax(layers) {
        return d3.max(layers, function (d) {
            return d[1];
        });
    }

    const main_g = svg.append('g')
        .selectAll('g')
        .data(layers);

    const g = main_g.enter().append('g')
        .attr('fill', function (d) {
            return color(d.key);
        });

    const rect = g.selectAll('rect')
        .data(function (d) {
            d.forEach(function (d1) {
                d1.key = d.key;
                return d1;
            });
            return d;
        })
        .enter().append('rect')
        .attr('data', function (d) {
            const data = {};
            data['key'] = d.key;
            data['value'] = d.data[d.key];
            let total = 0;
            group.map(function (d1) {
                total = total + d.data[d1]
            });
            data['total'] = total;
            return JSON.stringify(data);
        })
        .attr('width', function (d) {
            return x(d[1]) - x(d[0]);
        })
        .attr('x', function (d) {
            return x(d[0]);
        })
        .attr('height', y.bandwidth);

    function onMouseUpdate(e) {
        return tooltip.style('top', (e.pageY - 10) + 'px').style('left', (e.pageX + 10) + 'px');
    }

    document.addEventListener('mousemove', onMouseUpdate, false);
    document.addEventListener('mouseenter', onMouseUpdate, false);

    rect.on('mouseover', function (d) {
        tooltip.text(d.key + ': ' + d.data[d.key]);
        tooltip.style('visibility', 'visible');
    })
        .on('mousemove', function (event) {
            return tooltip.style('top', (event.pageY - 10) + 'px')
                .style('left', (event.pageX + 10) + 'px');
        })
        .on('mouseout', function () {
            tooltip.style('visibility', 'hidden');
        });
}


function expand(element_id, element) {
    $(element).html($(element).text().includes("Expand") ? $(element).html().replace('Expand', 'Collapse') : $(element).html().replace('Collapse', 'Expand'));
    element = document.getElementById(element_id);
    if (element.getAttribute('style').includes(' height'))
        element.setAttribute('style', 'overflow: hidden; overflow-wrap: break-word; min-height: 48px;');
    else autosize.update(element);

}


function checked(element) {
    const elem = $(element), selected = elem.html() === 'Selected';
    if (selected) elem.html("Select<a style='visibility: hidden'>ed</a>")
        .attr('class', elem.attr('class').replace('btn-secondary', 'btn-outline-secondary'));
    else elem.html('Selected')
        .attr('class', elem.attr('class').replace('btn-outline-secondary', 'btn-secondary'));
    elem.prev().select = selected;
}


function copyReport() {
    const dummy = $('#copy_result');
    dummy.removeAttr('hidden').select();
    document.execCommand("copy");
    alert("Copied the text: " + dummy.val());
    dummy.attr('hidden', '');
}