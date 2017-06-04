<row>
    <class if={classrow.length == 3} class="course text-justify rounded card column col-xs-12 col-sm-12 col-md-6 col-lg-4"
           each="{ classrow }"
           data="{ this }">
    </class>
    <class if={classrow.length == 1} style="max-width:33%;" class="hide-sm course float-left text-justify rounded card column col-xs-12 col-sm-12 col-md-12 col-lg-12"
           each="{ classrow }"
           data="{ this }">
    </class>
    <class if={classrow.length == 1} style="max-width:100%;" class="show-sm course float-left text-justify rounded card column col-md-12 col-lg-12"
           each="{ classrow }"
           data="{ this }">
    </class>
    <class if={classrow.length == 2} style="max-width:33%;" class="hide-sm course float-left text-justify rounded card column col-md-8 col-lg-8"
           each="{ classrow }"
           data="{ this }">
    </class>
    <class if={classrow.length == 2} style="max-width:100%;" class="show-sm course float-left text-justify rounded card column col-xs-12 col-sm-12"
           each="{ classrow }"
           data="{ this }">
    </class>

<script>
this.classrow = opts.classrow
</script>

</row>
